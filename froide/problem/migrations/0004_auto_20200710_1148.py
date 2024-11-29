# Generated by Django 3.0.8 on 2020-07-10 09:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("problem", "0003_auto_20190527_1410"),
    ]

    operations = [
        migrations.AddField(
            model_name="problemreport",
            name="claimed",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="problemreport",
            name="moderator",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="problems_moderated",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="problemreport",
            name="kind",
            field=models.CharField(
                choices=[
                    (
                        "bounce_publicbody",
                        "You received a bounce mail from the public agency.",
                    ),
                    ("message_not_delivered", "Your message was not delivered."),
                    ("attachment_broken", "The attachments don't seem to work."),
                    ("redaction_needed", "You need more redaction."),
                    (
                        "foi_help_needed",
                        "You need help to understand or reply to this message.",
                    ),
                    ("other", "Something else..."),
                    ("not_foi", "This is not a proper FOI request."),
                    ("redaction_needed", "More redactions are needed."),
                    ("not_nice", "Content is against netiquette."),
                    ("info_outdated", "Published information is outdated."),
                    ("info_wrong", "Published information is wrong."),
                    ("other", "Something else..."),
                ],
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="problemreport",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="problems_reported",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
