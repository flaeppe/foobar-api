# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-12 12:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_auto_20170309_1944'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='producttransactionstatus',
            options={'ordering': ('-date_created',), 'verbose_name': 'transaction status', 'verbose_name_plural': 'transaction statuses'},
        ),
        migrations.AlterField(
            model_name='delivery',
            name='date_created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True, verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='product',
            name='date_created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True, verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='producttransaction',
            name='date_created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True, verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='producttransactionstatus',
            name='date_created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True, verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='stocktake',
            name='date_created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True, verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='supplierproduct',
            name='date_created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True, verbose_name='date created'),
        ),
    ]
