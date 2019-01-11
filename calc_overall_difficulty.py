import numpy as np
import sys

'''
The aim is to 'predict' the accuracy a player (define by his player_level) would get on the map.

For that, a function giving the accuracy a player would get on a note with an individual_difficulty
 and then do the mean of all accuracy received (like it is calculated by the game).
The difficulty is then chosen too be the player_level needed to get 95% accuracy. 

The function is currently : https://www.desmos.com/calculator/5cagucvqbd

'''
k = 6


def accuracy_from_kps_and_player_level(x):
    return pow(np.tanh((x+0.00001) ** k) / (x+0.00001) ** k, 1 / k)


def calc_overall_difficulty(individual_difficulty):
    accuracy_at_player_level = 0
    player_level = 0.01
    player_level_95 = 0
    b = True
    accuracy_VS_player_level = []
    while accuracy_at_player_level < 0.99:
        accuracy_at_player_level = np.mean(accuracy_from_kps_and_player_level(individual_difficulty / player_level))
        accuracy_VS_player_level.append(accuracy_at_player_level)

        if b and accuracy_at_player_level > 0.95:
            player_level_95 = player_level
            b = False

        player_level += 0.001

    return accuracy_VS_player_level, player_level_95
