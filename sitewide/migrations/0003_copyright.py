# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-01 08:19
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sitewide', '0002_bio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Copyright',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', wagtail.wagtailcore.fields.RichTextField()),
            ],
        ),
    ]
