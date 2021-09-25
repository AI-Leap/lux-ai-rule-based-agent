from collections import defaultdict
from missions.mission import Mission
from lux.game_map import Position
from missions.mission_constants import MissionConstants
import missions.mission_service as MissionService


class Unit:
    def __init__(self, id, x, y):
        self.id = id
        self.pos = Position(x, y)


def test_delete_mission_without_unit():
    missions = defaultdict(dict)
    missions['u_1'] = {
        'mission_type': 'CITY_GUARD',
        'city_id': 'c_1',
        'target_pos': {
            'x': 0,
            'y': 0
        }
    }
    missions['u_2'] = {
        'mission_type': 'CITY_BUILDING',
        'city_id': 'c_1',
        'target_pos': {
            'x': 1,
            'y': 1
        }
    }
    missions['u_3'] = {
        'mission_type': MissionConstants.MissionType.RESOURCE_COLLECTION,
        'target_pos': {
            'x': 2,
            'y': 2
        }
    }

    units = ['u_1']

    updated_missions = MissionService.delete_mission_without_unit(
        missions,
        units
    )

    assert updated_missions == {
        'u_1': {
            'mission_type': 'CITY_GUARD',
            'city_id': 'c_1',
            'target_pos': {
                'x': 0,
                'y': 0
            }
        }
    }


def test_negotiate_missions():
    missions = defaultdict(Mission)
    missions['u_1'] = Mission(MissionConstants.MissionType.RESOURCE_COLLECTION)
    missions['u_1'].update_unit(Unit('u_1', 10, 4))

    missions['u_2'] = Mission(MissionConstants.MissionType.RESOURCE_COLLECTION)
    missions['u_2'].update_unit(Unit('u_2', 10, 5))

    missions['u_3'] = Mission(MissionConstants.MissionType.RESOURCE_COLLECTION)
    missions['u_3'].update_unit(Unit('u_3', 11, 5))

    target_positions = [
        Position(12, 3),
        Position(9, 6),
        Position(11, 7),
    ]

    missions = MissionService.negotiate_missions(
        missions,
        [mission.unit for _, mission in missions.items()],
        target_positions
    )

    assert isinstance(missions['u_1'], Mission)
    assert missions['u_1'].target_pos.equals(Position(12, 3))
    assert missions['u_2'].target_pos.equals(Position(9, 6))
    assert missions['u_3'].target_pos.equals(Position(11, 7))


def test_negotiate_missions2():
    missions = defaultdict(Mission)
    missions['u_1'] = Mission(MissionConstants.MissionType.RESOURCE_COLLECTION)
    missions['u_1'].update_unit(Unit('u_1', 2, 12))

    missions['u_2'] = Mission(MissionConstants.MissionType.RESOURCE_COLLECTION)
    missions['u_2'].update_unit(Unit('u_2', 5, 12))

    target_positions = [
        Position(0, 12),
        Position(0, 13),
        Position(0, 14),
    ]

    missions = MissionService.negotiate_missions(
        missions,
        [mission.unit for _, mission in missions.items()],
        target_positions
    )

    assert isinstance(missions['u_1'], Mission)
    assert missions['u_1'].target_pos.equals(Position(0, 12))
    assert missions['u_2'].target_pos.equals(Position(0, 13))


def test_negotiate_missions3():
    missions = defaultdict(Mission)
    missions['u_1'] = Mission(MissionConstants.MissionType.RESOURCE_COLLECTION)
    missions['u_1'].update_unit(Unit('u_1', 10, 2))

    missions['u_2'] = Mission(MissionConstants.MissionType.RESOURCE_COLLECTION)
    missions['u_2'].update_unit(Unit('u_2', 12, 2))

    missions['u_2'] = Mission(MissionConstants.MissionType.RESOURCE_COLLECTION)
    missions['u_2'].update_unit(Unit('u_2', 10, 3))

    target_positions = [
        Position(11, 0),
        Position(12, 0),
    ]

    missions = MissionService.negotiate_missions(
        missions,
        [mission.unit for _, mission in missions.items()],
        target_positions
    )

    assert isinstance(missions['u_1'], Mission)
    assert missions['u_1'].target_pos.equals(Position(11, 0))
    assert missions['u_2'].target_pos.equals(Position(12, 0))
