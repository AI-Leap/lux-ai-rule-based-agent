from lux.game_constants import GAME_CONSTANTS


def update_game_state_info(turn):
    MAX_DAYS = GAME_CONSTANTS['PARAMETERS']['MAX_DAYS']
    DAY_LENGTH = GAME_CONSTANTS['PARAMETERS']['DAY_LENGTH']
    NIGHT_LENGTH = GAME_CONSTANTS['PARAMETERS']['NIGHT_LENGTH']
    FULL_LENTH = DAY_LENGTH + NIGHT_LENGTH

    all_night_turns_lef = ((MAX_DAYS - 1 - turn) // FULL_LENTH + 1) \
        * NIGHT_LENGTH

    turns_to_night = (DAY_LENGTH - turn) % FULL_LENTH
    turns_to_night = 0 if turns_to_night > 30 else turns_to_night

    turns_to_dawn = FULL_LENTH - turn % FULL_LENTH
    turns_to_dawn = 0 if turns_to_dawn > 10 else turns_to_dawn

    is_day_time = turns_to_dawn == 0
    is_night_time = turns_to_night == 0

    if is_night_time:
        all_night_turns_lef -= (10 - turns_to_dawn)

    return {
        'all_night_turns_left': all_night_turns_lef,
        'turns_to_night': turns_to_night,
        'turns_to_dawn': turns_to_dawn,
        'is_day_time': is_day_time,
        'is_night_time': is_night_time
    }
