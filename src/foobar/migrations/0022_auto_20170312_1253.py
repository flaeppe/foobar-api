# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-12 12:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('foobar', '0021_remove_purchase_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchasestatus',
            options={'ordering': ('-date_created',), 'verbose_name': 'purchase status', 'verbose_name_plural': 'purchase statuses'},
        ),
        migrations.AlterField(
            model_name='account',
            name='date_created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True, verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='card',
            name='date_created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True, verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date_created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True, verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='purchasestatus',
            name='date_created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True, verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='walletlogentry',
            name='date_created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True, verbose_name='date created'),
        ),
    ]