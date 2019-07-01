#!/usr/bin/python
# -*- coding: UTF-8 -*-

from tqdm import tqdm

import statsbomb as sb

import numpy as np
from math import sqrt
from collections import defaultdict, Counter
import re
import random

from config import *

def wc_events(events, teams):
    res = []

    for i in tqdm(events):
        t = sb.Events(event_id=i)
        res.append((t.data[0]['team']['name'], t.data[1]['team']['name'], i))

    res = [item for item in res if item[0] in teams or item[1] in teams]
    return res

def preproc(df, play_patterns, height_patterns, data_col, labels_col, types_col, X, Y, norm=True):
    df.under_pressure = df.under_pressure.apply(lambda x: 1 if x else 0)
    df.play_pattern = df.play_pattern.apply(lambda x: play_patterns[x])
    df.height = df.height.apply(lambda x: height_patterns[x] / len(height_patterns))
    df.pass_backheel = df.pass_backheel.apply(lambda x: 1 if x else 0)
    df.miscommunication = df.miscommunication.apply(lambda x: 1 if x else 0)
    df.through_ball = df.through_ball.apply(lambda x: 1 if x else 0)
    df.cross = df.cross.apply(lambda x: 1 if x else 0)
    df.cut_back = df.cut_back.apply(lambda x: 1 if x else 0)
    df.switch = df.switch.apply(lambda x: 1 if x else 0)
    df.shot_assist = df.shot_assist.apply(lambda x: 1 if x else 0)
    df.goal_assist = df.goal_assist.apply(lambda x: 1 if x else 0)
    if norm:
        df.start_location_x = df.start_location_x.apply(lambda x: x / X)
        df.start_location_y = df.start_location_x.apply(lambda x: x / Y)
        df.end_location_x = df.start_location_x.apply(lambda x: x / X)
        df.end_location_y = df.start_location_x.apply(lambda x: x / Y)
        df.length = df.length.apply(lambda x: x / X)
    return df[data_col], df[labels_col], df[types_col]

def generate_dataset(res, data_col=data_col, play_patterns=play_patterns,
                     height_patterns=height_patterns, players_col=players_col,
                     types_col=types_col, X=X, Y=Y):
    data = pd.DataFrame(columns=data_col)
    players = pd.DataFrame(columns=players_col)
    types = pd.DataFrame(columns=types_col)

    for match_id in tqdm([x[2] for x in res]): # cur_res
        match = sb.Events(event_id=match_id)
        df = match.get_dataframe(event_type='pass')[columns]

        cur_data, cur_players, cur_types = preproc(df, play_patterns=play_patterns,
                                                   height_patterns=height_patterns, data_col=data_col,
                                                   labels_col=players_col, types_col=types_col, X=X, Y=Y)

        data = data.append(cur_data, ignore_index=True)
        players = players.append(cur_players, ignore_index=True)
        types = types.append(cur_types, ignore_index=True)

    data = data.sample(frac=1)
    ind = data.index
    players = players.reindex(ind)
    types = types.reindex(ind)

    data = data.reset_index(drop=True)
    players = players.reset_index(drop=True)
    types = types.reset_index(drop=True)
    return data, players, types

def create_players_data(players, min_p=100):
    player_c = Counter()
    all_players = [x[0] for x in players.values]
    for player in all_players:
        player_c[player] += 1
    players_list = [key for key, val in player_c.items() if val >= min_p]

    player2idx = {player: i for i, player in enumerate(players_list)}
    idx2player = {val: key for key, val in player2idx.items()}
    return players_list, player2idx, idx2player

def filter_data(players, data, players_list):
    players = players.loc[players.player.isin(players_list)]
    data = data.loc[data.index.isin(players.index)]
    players = players.reset_index(drop=True)
    data = data.reset_index(drop=True)
    return data, players

def create_positions(res):
    positions = defaultdict(list)
    for match_id in tqdm([x[2] for x in res]):
        match = sb.Events(event_id=match_id)
        for info in match.data[0]['tactics']['lineup']:
            positions[info['player']['name']].append(info['position']['name'])

        for info in match.data[1]['tactics']['lineup']:
            positions[info['player']['name']].append(info['position']['name'])

    positions = {key: Counter(val).most_common(1)[0][0] for key, val in positions.items()}
    pos_list = list(set(list(positions.values())))
    pos2id = {pos: i for i, pos in enumerate(pos_list)}
    return positions, pos_list, pos2id

def create_positions_id(pos_classes=pos_classes):
    pos2id_classes = {}
    for key, val in pos_classes.items():
        for v in val:
            pos2id_classes[v] = key
    return pos2id_classes

def make_positions_id(positions, pos2id_classes):
    return {key: pos2id_classes[val] for key, val in positions.items()}

def create_teams(res):
    teams = defaultdict(list)
    for match_id in tqdm([x[2] for x in res]):
        match = sb.Events(event_id=match_id)

        team = match.data[0]['possession_team']['name']
        for player in match.data[0]['tactics']['lineup']:
            teams[team].append(player['player']['name'])

        team = match.data[1]['possession_team']['name']
        for player in match.data[0]['tactics']['lineup']:
            teams[team].append(player['player']['name'])

    teams = {key: list(set(val)) for key, val in teams.items()}
    teams_vec = {key: sum([emb[x] for x in val if x in players_list]) / len([emb[x] for x in val if x in players_list])
                 for key, val in teams.items()}
    return teams, teams_vec
