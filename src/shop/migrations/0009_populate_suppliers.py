# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-11 20:08
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings

from narlivs import Narlivs


def populate_suppliers(apps, schema_editor):
    Supplier = apps.get_model("shop", "Supplier")
    SupplierProduct = apps.get_model("shop", "SupplierProduct")
    Product = apps.get_model("shop", "Product")

    products = Product.objects.all()

    if not products:
        return

    narlivs = Narlivs(settings.NARLIVS_USERNAME, settings.NARLIVS_PASSWORD)
    s = Supplier.objects.create(name='Närlivs', internal_name='narlivs')

    for p in products:
        try:
            data = narlivs.get_product(ean=p.code).data
        except:
            continue
        SupplierProduct.objects.create(
            supplier=s,
            product_id=p.id,
            name=p.name,
            sku=data['sku'],
            price=data['price']
        )


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_remove_producttransaction_reference_old'),
    ]

    operations = [
        migrations.RunPython(populate_suppliers)
    ]
