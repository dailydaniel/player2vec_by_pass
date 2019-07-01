#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import argparse

import statsbomb as sb
from tqdm import tqdm
import re
import random
import numpy as np
from math import sqrt
from collections import defaultdict, Counter
import pandas as pd

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from scipy.spatial import distance
from math import pi

import pickle

from model import *
from preproc import *
from config import *
from embedding import *

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--num_epoch', default=25, type=int)
    parser.add_argument('-m', '--min_passes', default=100, type=int)
    parser.add_argument('-d', '--embedding_dim', default=16, type=int)
    return parser

if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    res = wc_events(events, teams)
    data, players, _ = generate_dataset(res, data_col, play_patterns,
                                        height_patterns, players_col, types_col,
                                        X=X, Y=Y)
    players_list, player2idx, idx2player = create_players_data(players,
                                                               namespace.min_passes)
    data, players = filter_data(players, data, players_list)

    EMBEDDING_DIM = namespace.embedding_dim
    VOCABULARY_SIZE = len(players_list)
    INPUT_SIZE = len(data_col)

    model = Pass2Vec(EMBEDDING_DIM, INPUT_SIZE, VOCABULARY_SIZE)
    loss_function = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4, weight_decay=1e-5)

    model, avg_loss = train(model, data, players, player2idx, loss_function,
                            optimizer, namespace.num_epoch)

    emb = Embedding(model, players_list, player2idx)

    teams, teams_vec = create_teams(res)
    team_emb = TeamEmbedding(teams_vec)

    save(model, emb, team_emb)
