from foobar.exceptions import InvalidTransition


def validate_transition(enum, from_state, to_state):
    if not hasattr(enum, '_transitions'):
        raise InvalidTransition

    transitions = enum._transitions.value
    if to_state.value not in transitions.get(from_state.value, []):
        raise InvalidTransition
