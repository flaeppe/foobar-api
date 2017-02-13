# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-12 09:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields
import shop.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('shop', '0006_auto_20160919_1224'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date created')),
                ('date_modified', models.DateTimeField(auto_now=True, null=True, verbose_name='date modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('report', models.FileField(storage=shop.models.OverwriteFileSystemStorage(), upload_to=shop.models.generate_delivery_report_filename)),
            ],
            options={
                'verbose_name': 'Delivery',
                'verbose_name_plural': 'Deliveries',
            },
        ),
        migrations.CreateModel(
            name='DeliveryItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('qty', models.PositiveIntegerField()),
                ('price_currency', djmoney.models.fields.CurrencyField(choices=[('SEK', 'SEK')], default='SEK', editable=False, max_length=3)),
                ('price', djmoney.models.fields.MoneyField(blank=True, currency_choices=(('SEK', 'SEK'),), decimal_places=2, default=None, max_digits=10, null=True)),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_items', to='shop.Delivery')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
                ('internal_name', models.CharField(max_length=32)),
            ],
            options={
                'verbose_name': 'supplier',
                'verbose_name_plural': 'suppliers',
            },
        ),
        migrations.CreateModel(
            name='SupplierProduct',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date created')),
                ('date_modified', models.DateTimeField(auto_now=True, null=True, verbose_name='date modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('sku', models.CharField(max_length=32, verbose_name='SKU')),
                ('price_currency', djmoney.models.fields.CurrencyField(choices=[('SEK', 'SEK')], default='SEK', editable=False, max_length=3)),
                ('price', djmoney.models.fields.MoneyField(blank=True, currency_choices=(('SEK', 'SEK'),), decimal_places=2, default=None, max_digits=10, null=True)),
                ('image', models.ImageField(blank=True, null=True, storage=shop.models.OverwriteFileSystemStorage(), upload_to=shop.models.generate_supplier_product_filename)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supplier_products', to='shop.Product')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.Supplier')),
            ],
            options={
                'verbose_name': 'supplier product',
                'verbose_name_plural': 'supplier products',
            },
        ),
        migrations.RenameField(
            model_name='producttransaction',
            old_name='reference',
            new_name='reference_old',
        ),
        migrations.AddField(
            model_name='producttransaction',
            name='reference_ct',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='producttransaction',
            name='reference_id',
            field=models.UUIDField(blank=True, default=uuid.uuid4, null=True),
        ),
        migrations.AddField(
            model_name='deliveryitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='delivery_item', to='shop.SupplierProduct'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='items',
            field=models.ManyToManyField(through='shop.DeliveryItem', to='shop.SupplierProduct'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deliveries', to='shop.Supplier'),
        ),
        migrations.AlterUniqueTogether(
            name='supplierproduct',
            unique_together=set([('supplier', 'sku')]),
        ),
    ]