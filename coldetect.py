def check_player_hit(player_x, enemy_x, player_y, enemy_y):
    if enemy_x - 76 < player_x < enemy_x + 76:
        x_hit = True
    else:
        x_hit = False
    if enemy_y - 48 < player_y < enemy_y + 48:
        y_hit = True
    else:
        y_hit = False
    if y_hit is True and x_hit is True:
        return True
    return False


def check_beam_hit(beam_x, enemy_x, beam_y, enemy_y):
    if enemy_x - 36 < beam_x < enemy_x + 36:
        x_hit = True
    else:
        x_hit = False
    if enemy_y - 26 < beam_y < enemy_y + 26:
        y_hit = True
    else:
        y_hit = False
    if y_hit is True and x_hit is True:
        return True
    return False

