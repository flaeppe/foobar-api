import random
import factory.fuzzy
from .. import models
from moneyed import Money


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Account


class CardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Card

    account = factory.SubFactory(AccountFactory)
    number = factory.fuzzy.FuzzyInteger(0, (1 << 32) - 1)


class PurchaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Purchase

    account = factory.SubFactory(AccountFactory)
    amount = factory.fuzzy.FuzzyInteger(0, 1337)


class PurchaseItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PurchaseItem

    purchase = factory.SubFactory(PurchaseFactory)
    product_id = ''
    qty = 1

    @factory.lazy_attribute
    def amount(self):
        return Money(random.randint(1, 100), 'SEK')


class PurchaseStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PurchaseStatus

    purchase = factory.SubFactory(PurchaseFactory)
