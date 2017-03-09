import factory.fuzzy
from .. import models


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


class PurchaseStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PurchaseStatus

    purchase = factory.SubFactory(PurchaseFactory)
