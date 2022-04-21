import pickle

import numpy as np
import requests
from flask import Flask
import games_stats_factory
import json
import game_stats
import ast
from refresh_data import Game

app = Flask(__name__)


class Game:
    def __init__(self, game_stats):
        self.game = game_stats
        self.comeback = game_stats.get_score_greatest_comeback()
        self.close_game = game_stats.get_score_close_game()
        self.best_teams = game_stats.get_score_best_teams()
        self.personal_performance = game_stats.get_score_personal_performance()
        self.high_game_rate = game_stats.get_score_game_rate()


games_stats = games_stats_factory.get_games_stats()
games = []
for game in games_stats:
    games.append(Game(game))


@app.route("/<arg>")
def get_best_game(arg):
    predict = False
    if "predict" in arg:
        arg = arg[len("predict"):]
        predict = True
        print("predict")
    print(arg)
    # with open("games.gms", "rb") as f:
    #     games = pickle.load(f)
    biggest_score = -np.inf
    pref = arg.split(";")
    pref = list(filter(bool, pref))
    pref_dict = {}
    for p in pref:
        cur_pref = p.split("=")
        pref_dict[cur_pref[0]] = cur_pref[1]
    best_score = None
    # with open("games.pkl", "rb") as f:
    #     games = pickle.load(f)
    for game_class in games:
        score = 0
        if 'Great comeback' in pref_dict:
            score += int(pref_dict['Great comeback']) * game_class.comeback
        if 'Close game' in pref_dict:
            score += int(pref_dict['Close game']) * game_class.close_game
        if 'Good teams' in pref_dict:
            score += int(pref_dict['Good teams']) * game_class.best_teams
        if 'High game rate' in pref_dict:
            score += int(pref_dict['High game rate']) * game_class.high_game_rate
        if 'personal performance' in pref_dict:
            score += int(pref_dict['personal performance']) * game_class.personal_performance

        # print("score= ", score)
        if score > biggest_score:
            biggest_score = score
            best_score = game_class.game
    json_response = {}
    if best_score is None:
        json_response["response_tag"] = -1
    else:
        json_response["response_tag"] = 1
        json_response["team_1_id"] = int(best_score.line_score.TEAM_ID[0])
        json_response["team_2_id"] = int(best_score.line_score.TEAM_ID[1])
    # print("biggest score = ", biggest_score)
    print("return")
    return json.dumps(json_response)


if __name__ == "__main__":
    # app.debug = True
    app.run(host='0.0.0.0')  # initialize server
