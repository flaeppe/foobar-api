from foobar.exceptions import InvalidTransition


def validate_transition(enum, from_state, to_state):
    if not hasattr(enum, '_transitions'):
        raise InvalidTransition('No transitions found')

    transitions = enum._transitions.value
    from_value = from_state.value if from_state is not None else None
    if to_state.value not in transitions.get(from_value, []):
        msg = 'Transition {0} -> {1} not allowed'.format(from_state, to_state)
        raise InvalidTransition(msg)


def get_direction_multiplier(enum, from_state, to_state, direction):
    if not hasattr(enum, '_money_transitions'):
        raise InvalidTransition('No money transitions found')

    transitions = enum._money_transitions.value.get(direction)
    if transitions is None:
        msg = 'No transitions found for direction: {0}'.format(direction)
        raise InvalidTransition(msg)

    from_key = from_state.value if from_state is not None else None
    to_key = to_state.value if to_state is not None else None
    return transitions.get((from_key, to_key))
