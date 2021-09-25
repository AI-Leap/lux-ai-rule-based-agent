def get_unit_by_id(id, units):
    unit = next(
        (unit for unit in units if unit.id == id), None
    )
    return unit
