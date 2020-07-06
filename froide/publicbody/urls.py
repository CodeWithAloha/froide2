from django.conf.urls import url
from django.utils.translation import pgettext_lazy

from .views import (
    PublicBodySearch, PublicBodyProposalView, PublicBodyChangeView
)


urlpatterns = [
    url(pgettext_lazy('url part', r"^propose/$"),
        PublicBodyProposalView.as_view(), name="publicbody-propose"),

    url(pgettext_lazy('url part', r"^change/(?P<pk>\d+)/$"),
        PublicBodyChangeView.as_view(), name="publicbody-change"),

    url(r"^$", PublicBodySearch.as_view(), name="publicbody-list"),
    # Translators: part in Public Body URL
    url(pgettext_lazy('url part', r"^topic/(?P<category>[-\w]+)/$"),
            PublicBodySearch.as_view(), name="publicbody-list"),
    url(r"^(?P<jurisdiction>[-\w]+)/$",
            PublicBodySearch.as_view(), name="publicbody-list"),
    # Translators: part in Public Body URL
    url(pgettext_lazy('url part', r"^(?P<jurisdiction>[-\w]+)/topic/(?P<category>[-\w]+)/$"),
            PublicBodySearch.as_view(), name="publicbody-list"),
]
