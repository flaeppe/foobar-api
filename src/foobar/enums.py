import enum


class PurchaseStatus(enum.Enum):
    FINALIZED = 0
    CANCELED = 1
    PENDING = 2

    _transitions = {
        FINALIZED: (CANCELED,),
        PENDING: (FINALIZED, CANCELED)
    }


class TrxType(enum.Enum):
    CORRECTION = 0
    DEPOSIT = 1
    WITHDRAWAL = 2
