# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-09 19:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_auto_20170309_1935'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producttransaction',
            name='reference_ct',
        ),
        migrations.RemoveField(
            model_name='producttransaction',
            name='reference_id',
        ),
        migrations.RemoveField(
            model_name='producttransaction',
            name='trx_status',
        ),
    ]
