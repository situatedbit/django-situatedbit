# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-10 09:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basepage',
            name='in_home_stream',
        ),
    ]
