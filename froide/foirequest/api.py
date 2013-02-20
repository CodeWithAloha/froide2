from django.conf.urls.defaults import url
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404

from haystack.query import SearchQuerySet
from tastypie.paginator import Paginator as TastyPaginator
from tastypie.resources import ModelResource
from tastypie import fields, utils
from tastypie.constants import ALL
from tastypie.authorization import DjangoAuthorization

from froide.helper.api_utils import AnonymousGetAuthentication

from .models import FoiRequest, FoiMessage, FoiAttachment


class FoiAttachmentResource(ModelResource):
    class Meta:
        allowed_methods = ['get', 'put', 'post', 'delete']
        queryset = FoiAttachment.objects.filter(belongs_to__request__visibility=2, approved=True)
        resource_name = 'attachment'
        authentication = AnonymousGetAuthentication()
        authorization = DjangoAuthorization()


class FoiMessageResource(ModelResource):
    attachments = fields.ToManyField(FoiAttachmentResource,
        'foiattachment_set', full=True, related_name='belongs_to')
    recipient_public_body = fields.ToOneField(
        'froide.publicbody.api.PublicBodyResource',
        'recipient_public_body', null=True)
    sender_public_body = fields.ToOneField(
        'froide.publicbody.api.PublicBodyResource',
        'sender_public_body', null=True)

    class Meta:
        allowed_methods = ['get', 'put', 'delete']
        queryset = FoiMessage.objects.filter(request__visibility=2)
        resource_name = 'message'
        fields = ['request', 'sent', 'is_response', 'is_postal',
            'is_escalation', 'content_hidden', 'sender_public_body',
            'recipient_public_body', 'status', 'timestamp',
            'redacted', 'not_publishable'
        ]
        authentication = AnonymousGetAuthentication()
        authorization = DjangoAuthorization()

    def dehydrate(self, bundle):
        if bundle.obj:
            bundle.data.update({
                'subject': bundle.obj.get_subject(),
                # FIXME: encapsulate that logic
                'content': bundle.obj.get_content() if not bundle.obj.content_hidden else None,
                'sender': bundle.obj.sender,
                'status_name': FoiRequest.get_status_description(
                    bundle.obj.status)
            })
        return bundle


class FoiRequestResource(ModelResource):
    public_body = fields.ToOneField('froide.publicbody.api.PublicBodyResource', 'public_body', null=True)
    messages = fields.ToManyField(FoiMessageResource, 'foimessage_set',
        full=True, related_name='request')
    same_as = fields.ToOneField('froide.foirequest.api.FoiRequestResource',
        'same_as', null=True)
    law = fields.ToOneField('froide.publicbody.api.FoiLawResource',
        'law', null=True)
    jurisdiction = fields.ToOneField(
        'froide.publicbody.api.JurisdictionResource',
        'jurisdiction', null=True)

    class Meta:
        allowed_methods = ['get', 'put']
        queryset = FoiRequest.objects.filter(visibility=2)
        resource_name = 'request'
        fields = [
            'jurisdiction',
            'is_foi', 'checked', 'refusal_reason',
            'costs',
            'public',
            'law',
            'same_as_count',
            'same_as',
            'due_date',
            'resolved_on', 'last_message', 'first_message',
            'status',
            'public_body',
            'resolution', 'slug',
            'title'
        ]
        filtering = {
            "slug": ('exact', 'startswith',),
            "title": ALL,
        }
        authentication = AnonymousGetAuthentication()
        authorization = DjangoAuthorization()
        paginator_class = TastyPaginator

    def dehydrate(self, bundle):
        if bundle.obj:
            bundle.data['description'] = bundle.obj.get_description()
            bundle.data['status_name'] = bundle.obj.readable_status
            bundle.data['tags'] = [{'slug': t.slug, 'name': t.name}
                for t in bundle.obj.tags.all()
            ]
        return bundle

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, utils.trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
        ]

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])

        # Do the query.
        sqs = SearchQuerySet().models(FoiRequest).load_all().auto_query(request.GET.get('q', ''))
        paginator = Paginator(sqs, 20)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        objects = []

        for result in page.object_list:
            bundle = self.build_bundle(obj=result.object, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        return self.create_response(request, object_list)
