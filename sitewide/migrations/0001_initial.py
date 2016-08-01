# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-01 07:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FooterLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('text', models.CharField(max_length=255)),
                ('title', models.CharField(blank=True, max_length=512)),
            ],
        ),
    ]
