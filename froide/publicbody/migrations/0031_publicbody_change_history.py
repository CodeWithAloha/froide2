# Generated by Django 3.0.8 on 2020-07-30 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicbody', '0030_auto_20200721_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicbody',
            name='change_history',
            field=models.JSONField(blank=True, default=list),
        ),
    ]