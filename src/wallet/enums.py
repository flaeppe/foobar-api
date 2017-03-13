import enum


class TrxDirection(enum.Enum):
    INCOMING = 0
    OUTGOING = 1


class TrxStatus(enum.Enum):
    FINALIZED = 0
    PENDING = 1
    CANCELLATION = 2

    _transitions = {
        None: (PENDING,),
        PENDING: (FINALIZED, CANCELLATION),
        FINALIZED: (CANCELLATION,)
    }

    _money_transitions = {
        TrxDirection.OUTGOING: {
            (None, PENDING): 1,
            (PENDING, FINALIZED): 0,
            (PENDING, CANCELLATION): -1,
            (FINALIZED, CANCELLATION): -1
        },
        TrxDirection.INCOMING: {
            (None, PENDING): 0,
            (PENDING, FINALIZED): 1,
            (PENDING, CANCELLATION): 0,
            (FINALIZED, CANCELLATION): -1
        }
    }
