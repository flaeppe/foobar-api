from foobar.exceptions import InvalidTransition


def validate_transition(enum, from_state, to_state):
    if not hasattr(enum, '_transitions'):
        raise InvalidTransition('No transitions found')

    transitions = enum._transitions.value
    if to_state.value not in transitions.get(from_state.value, []):
        msg = 'Transition {0} -> {1} not allowed'.format(from_state, to_state)
        raise InvalidTransition(msg)
