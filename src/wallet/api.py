from django.db import transaction
from .enums import TrxType
from . import models, exceptions


def get_wallet(owner_id, currency):
    """Return a wallet for given owner id.

    Creates a wallet if there is not one.
    """
    obj, created = models.Wallet.objects.get_or_create(
        owner_id=owner_id,
        balance_currency=currency
    )
    return obj


def get_balance(owner_id, currency, cached=True):
    """Return balance of the wallet and the wallet itself.

    Calculated by summing together all the PENDING/FINALIZED transactions
    in the wallet.
    """
    wallet_obj = get_wallet(owner_id, currency)
    if not cached:
        return wallet_obj, wallet_obj.transactions.balance()
    return wallet_obj, wallet_obj.balance


@transaction.atomic
def set_balance(owner_id, new_balance, reference=None):
    wallet, old_balance = get_balance(owner_id, new_balance.currency)
    difference = new_balance - old_balance
    if difference.amount < 0:
        trx_obj = withdraw(owner_id, -difference, reference)
        trx_obj = finalize_transaction(trx_obj.pk)
        return trx_obj, difference

    elif difference.amount > 0:
        trx_obj = deposit(owner_id, difference, reference)
        trx_obj = finalize_transaction(trx_obj.pk)
        return trx_obj, difference
    return None, difference


def list_transactions(owner_id, currency, trx_type=None, direction=None,
                      start=None, limit=None):
    """Return a list of transactions matching the criteria."""
    wallet_obj = get_wallet(owner_id, currency)
    qs = models.Wallet.objects.get(id=wallet_obj.id).transactions
    if trx_type is not None:
        # qs = qs.filter(trx_type=trx_type)
        qs = qs.by_status(trx_type)
    if direction is not None:
        qs = qs.by_direction(direction)
    return qs.all()[start:limit]


def total_balance(currency, exclude_ids=None):
    """Returns the total balance of the system"""
    qs = models.Wallet.objects.filter(balance_currency=currency)
    if exclude_ids is not None:
        qs = qs.exclude(owner_id__in=exclude_ids)
    return qs.sum(currency)


def get_transactions_by_ref(reference):
    """Return transactions with given reference."""
    return models.WalletTransaction.objects.filter(reference=reference)


def cancel_transaction(trx_id):
    """Cancels a transaction."""
    trx_obj = models.WalletTransaction.objects.get(id=trx_id)
    trx_obj.set_status(TrxType.CANCELLATION)
    return trx_obj


def finalize_transaction(trx_id):
    """Finalizes a transaction."""
    trx_obj = models.WalletTransaction.objects.get(id=trx_id)
    trx_obj.set_status(TrxType.FINALIZED)
    return trx_obj


@transaction.atomic
def finalize_transactions(trx_list):
    return [finalize_transaction(trx_id) for trx_id in trx_list]


@transaction.atomic
def withdraw(owner_id, amount, reference=None):
    """Withdraw given amount from the wallet.

    Throw InsufficientFunds if there is not enough money in the wallet.
    """
    assert amount.amount > 0, "The amount must be positive."
    wallet_obj, balance = get_balance(owner_id, amount.currency)
    if amount > balance:
        raise exceptions.InsufficientFunds
    qs = models.Wallet.objects.get(id=wallet_obj.id).transactions
    trx_obj = qs.create(amount=(-amount), reference=reference)
    trx_obj.set_status(TrxType.PENDING)
    return trx_obj


@transaction.atomic
def deposit(owner_id, amount, reference=None):
    """Deposit given amount into the wallet."""
    assert amount.amount > 0, "The amount must be positive."
    wallet_obj = get_wallet(owner_id, amount.currency)
    qs = models.Wallet.objects.get(id=wallet_obj.id).transactions

    trx_obj = qs.create(amount=amount, reference=reference)
    trx_obj.set_status(TrxType.PENDING)
    return trx_obj


@transaction.atomic
def transfer(debtor_id, creditor_id, amount, reference=None):
    """Withdraw money from debtor's wallet and deposit it into creditor's"""
    withdrawal_trx = withdraw(debtor_id, amount, reference)
    deposit_trx = deposit(creditor_id, amount, reference)
    return withdrawal_trx, deposit_trx
