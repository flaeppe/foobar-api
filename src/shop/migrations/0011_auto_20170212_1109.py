# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-12 11:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_delivery_processed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='delivery',
            old_name='processed',
            new_name='locked',
        ),
    ]
