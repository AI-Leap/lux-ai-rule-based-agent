def get_opponent_citytiles_positions(opponent):
    citytiles = []
    for city in opponent.cities.values():
        for city_tile in city.citytiles:
            citytiles.append(city_tile)

    return [ct.pos for ct in citytiles]


def get_opponent_citytiles(opponent):
    citytiles = []
    for city in opponent.cities.values():
        for city_tile in city.citytiles:
            citytiles.append(city_tile)

    return citytiles


def get_opponent_units_positions(opponent):
    return [u.pos for u in opponent.units]
