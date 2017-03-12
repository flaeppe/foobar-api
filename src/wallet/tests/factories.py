import uuid
import factory.fuzzy
from .. import models, enums
from ..signals.signals import status_change
from moneyed import Money


class FuzzyMoney(factory.fuzzy.FuzzyDecimal):
    def fuzz(self):
        return Money(super().fuzz(), 'SEK')


class WalletFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Wallet

    owner_id = factory.Sequence(lambda n: str(uuid.uuid4()))
    balance = Money(0, 'SEK')


class WalletTrxFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WalletTransaction

    wallet = factory.SubFactory(WalletFactory)
    amount = FuzzyMoney(0, 100000)


class WalletTrxStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WalletTransactionStatus

    trx = factory.SubFactory(WalletTrxFactory)
    status = enums.TrxType.FINALIZED


class WalletTrxWithStatusFactory(WalletTrxFactory):
    states = factory.RelatedFactory(
        WalletTrxStatusFactory,
        'trx',
        status=enums.TrxType.FINALIZED
    )


def pend_trx(trx, direction=enums.TrxDirection.INCOMING):
    assert trx.states.all().count() == 0
    pending_status = trx.states.create(status=enums.TrxType.PENDING)
    status_change.send(
        sender=pending_status.__class__,
        instance=pending_status,
        from_status=None,
        to_status=enums.TrxType.PENDING,
        direction=direction
    )


def finalize_trx(trx, direction=enums.TrxDirection.INCOMING):
    assert trx.states.all().count() == 0
    pend_trx(trx, direction)

    finalized_status = trx.states.create(status=enums.TrxType.FINALIZED)
    status_change.send(
        sender=finalized_status.__class__,
        instance=finalized_status,
        from_status=enums.TrxType.PENDING,
        to_status=enums.TrxType.FINALIZED,
        direction=direction
    )


def cancel_trx(trx, direction=enums.TrxDirection.INCOMING, pend=True):
    assert trx.states.all().count() == 0
    if pend:
        pend_trx(trx, direction)
    else:
        finalize_trx(trx, direction)

    canceled_status = trx.states.create(status=enums.TrxType.CANCELLATION)
    status_change.send(
        sender=canceled_status.__class__,
        instance=canceled_status,
        from_status=enums.TrxType.PENDING if pend else enums.TrxType.FINALIZED,
        to_status=enums.TrxType.CANCELLATION,
        direction=direction
    )
