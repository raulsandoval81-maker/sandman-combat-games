from game.settings import TECH_SCORE

def award_points(player, points):
    player.score += points
    player.actions += 1

def check_tech_fall(green, red):
    score_difference = green.score - red.score
    if score_difference >= TECH_SCORE:
        return "GREEN WINS!"
    if score_difference <= -TECH_SCORE:
        return "RED WINS!"
    return None

def decision_winner(green, red):
    if green.score > red.score:
        return "GREEN WINS BY DECISION!"
    if red.score > green.score:
        return "RED WINS BY DECISION!"
    return "DRAW!"
