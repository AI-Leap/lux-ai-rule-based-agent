from typing import List
from lux import annotate
from missions.mission import Mission
from missions.mission_constants import MissionConstants


def get_mission_annotations(missions: List[Mission]):
    annotations = []

    for key in missions:
        if missions[key].target_pos is None or \
                missions[key].unit is None:
            continue

        if missions[key].mission_type == \
                MissionConstants.MissionType.CLUSTER_GUARD and \
                missions[key].target_pos is not None:
            annotations.append(
                annotate.circle(
                    missions[key].target_pos.x,
                    missions[key].target_pos.y,
                )
            )
            annotations.append(
                annotate.line(
                    missions[key].unit.pos.x,
                    missions[key].unit.pos.y,
                    missions[key].target_pos.x,
                    missions[key].target_pos.y,
                )
            )

        if missions[key].mission_type == \
                MissionConstants.MissionType.BUILD_CITY_TILE and \
                missions[key].target_pos is not None:

            annotations.append(
                annotate.x(
                    missions[key].target_pos.x,
                    missions[key].target_pos.y,
                )
            )
            annotations.append(
                annotate.line(
                    missions[key].unit.pos.x,
                    missions[key].unit.pos.y,
                    missions[key].target_pos.x,
                    missions[key].target_pos.y,
                )
            )

        if missions[key].mission_type == \
                MissionConstants.MissionType.EXPLORATION and \
                missions[key].target_pos is not None:

            annotations.append(
                annotate.line(
                    missions[key].unit.pos.x,
                    missions[key].unit.pos.y,
                    missions[key].target_pos.x,
                    missions[key].target_pos.y,
                )
            )
            annotations.append(
                annotate.x(
                    missions[key].target_pos.x,
                    missions[key].target_pos.y,
                )
            )
            annotations.append(
                annotate.circle(
                    missions[key].target_pos.x,
                    missions[key].target_pos.y,
                )
            )

    return annotations
