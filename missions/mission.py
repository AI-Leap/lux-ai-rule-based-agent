from lux.game_objects import Unit
from lux.game_map import Position


class Mission:
    def __init__(self, mission_type: str):
        self.mission_type = mission_type
        self.target_pos = None
        self.unit = None
        self.allow_target_overwrite = True

    def update_unit(self, unit: Unit):
        self.unit = unit

    def update_target_pos(self, target_pos: Position):
        self.target_pos = target_pos
