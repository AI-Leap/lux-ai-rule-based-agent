from lux.game_map import Position
import actuators.actuator_service as ActuatorService


def test_get_all_directions():
    src = Position(0, 0)
    dest = Position(5, 5)
    directions = ActuatorService.get_all_directions(src, dest)
    assert directions == ['s', 'e']

    src = Position(0, 0)
    dest = Position(5, 0)
    directions = ActuatorService.get_all_directions(src, dest)
    assert directions == ['e']

    src = Position(5, 0)
    dest = Position(0, 0)
    directions = ActuatorService.get_all_directions(src, dest)
    assert directions == ['w']

    src = Position(5, 5)
    dest = Position(0, 0)
    directions = ActuatorService.get_all_directions(src, dest)
    assert directions == ['n', 'w']

    src = Position(0, 5)
    dest = Position(0, 0)
    directions = ActuatorService.get_all_directions(src, dest)
    assert directions == ['n']

    src = Position(0, 5)
    dest = Position(0, 10)
    directions = ActuatorService.get_all_directions(src, dest)
    assert directions == ['s']
