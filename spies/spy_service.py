def get_enemy_coverage(cells, opponent, opponent_id):
    '''
    This returns the number of opponent units and
    the number of citytiles in a list of cells given.
    '''
    opponent_citytiles = []
    for cell in cells:
        if cell.citytile is not None:
            if cell.citytile.team == opponent_id:
                opponent_citytiles.append(cell.citytile)

    cell_positions = [cell.pos for cell in cells]
    opponent_units = []
    for unit in opponent.units:
        pos = next(
            (p for p in cell_positions if p.equals(unit.pos)),
            None,
        )

        if pos is not None:
            opponent_units.append(unit)

    return opponent_citytiles, opponent_units
