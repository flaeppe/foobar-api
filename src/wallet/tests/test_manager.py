from django.test import TestCase
from moneyed import Money

from .. import enums, models
from .factories import (
    cancel_trx,
    finalize_trx,
    pend_trx,
    WalletTrxFactory,
    WalletFactory
)


class TransactionManagerTests(TestCase):
    def test_compute_balances(self):
        wallet_obj = WalletFactory.create()
        wallet_obj1 = WalletFactory.create()
        # INCOMING FINALIZED -> Supposed to count
        # 200
        trxs = WalletTrxFactory.create_batch(
            wallet=wallet_obj,
            size=2,
            amount=Money(100, wallet_obj.currency)
        )
        [finalize_trx(x) for x in trxs]
        # INCOMING PENDING -> NOT Supposed to count
        # 0
        trxs = WalletTrxFactory.create_batch(
            wallet=wallet_obj1,
            size=2,
            amount=Money(100, wallet_obj.currency)
        )
        [pend_trx(x) for x in trxs]
        # OUTGOING FINALIZED -> Supposed to count
        # -200
        trxs = WalletTrxFactory.create_batch(
            size=2,
            amount=-Money(100, wallet_obj.currency)
        )
        [finalize_trx(x, direction=enums.TrxDirection.OUTGOING) for x in trxs]
        # OUTGOING PENDING -> Supposed to count
        # -20
        trxs = WalletTrxFactory.create_batch(
            size=2,
            amount=-Money(10, wallet_obj.currency)
        )
        [pend_trx(x, direction=enums.TrxDirection.OUTGOING) for x in trxs]
        # INCOMING CANCELED -> NOT Supposed to count
        # 0
        trxs = WalletTrxFactory.create_batch(
            wallet=wallet_obj1,
            size=2,
            amount=Money(200, wallet_obj.currency)
        )
        [cancel_trx(x, pend=True) for x in trxs]
        # OUTGOING CANCELED -> NOT Supposed to count
        # 0
        trxs = WalletTrxFactory.create_batch(
            wallet=wallet_obj,
            size=2,
            amount=-Money(200, wallet_obj.currency)
        )
        [cancel_trx(x, enums.TrxDirection.OUTGOING, pend=False) for x in trxs]

        result = models.WalletTransaction.objects.countable()
        self.assertEqual(result.count(), 6)

        system_balance = result.balance()
        self.assertEqual(system_balance, Money(-20, wallet_obj.currency))

        balance = wallet_obj.transactions.balance()
        balance1 = wallet_obj1.transactions.balance()

        self.assertEqual(balance, Money(200, wallet_obj.currency))
        self.assertEqual(balance1, Money(0, wallet_obj1.currency))

    def test_filter_transaction_by_status(self):
        wallet_obj = WalletFactory.create()
        trxs = WalletTrxFactory.create_batch(
            size=3,
            amount=Money(100, wallet_obj.currency)
        )
        [pend_trx(x) for x in trxs]

        trxs = WalletTrxFactory.create_batch(
            size=4,
            amount=Money(50, wallet_obj.currency)
        )
        [finalize_trx(x) for x in trxs]

        trxs = WalletTrxFactory.create_batch(
            size=5,
            amount=Money(33, wallet_obj.currency)
        )
        [cancel_trx(x) for x in trxs]

        result = models.WalletTransaction.objects.by_status(status=None)
        self.assertEqual(result.count(), 12)

        status = enums.TrxType.PENDING
        result = models.WalletTransaction.objects.by_status(status=status)
        self.assertEqual(result.count(), 3)

        status = enums.TrxType.FINALIZED
        result = models.WalletTransaction.objects.by_status(status=status)
        self.assertEqual(result.count(), 4)

        status = enums.TrxType.CANCELLATION
        result = models.WalletTransaction.objects.by_status(status=status)
        self.assertEqual(result.count(), 5)
