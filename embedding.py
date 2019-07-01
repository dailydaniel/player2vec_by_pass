#!/usr/bin/python
# -*- coding: UTF-8 -*-

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

import matplotlib.pyplot as plt
from matplotlib import collections as mc

from scipy.spatial import distance
from math import pi


def idx2tensor(idx, n):
    x = torch.zeros(n).float()
    x[idx] = 1.0
    return x

class Embedding(object):
    def __init__(self, model, players_list, player2idx):
        with torch.no_grad():
            self.weight = model.fc2.weight.detach().numpy()
        self.emb = {}
        self.create_embedding(players_list, player2idx)

    def create_embedding(self, players_list, player2idx):
        with torch.no_grad():
            for player in players_list:
                self.emb[player] = idx2tensor(player2idx[player], VOCABULARY_SIZE).numpy() @ self.weight

    def __getitem__(self, key):
        return self.emb[key]

    def dist(self, a, b, vec=False):
        if vec:
            return 1.0 - distance.cosine(a, b)
        else:
            return 1.0 - distance.cosine(self.emb[a], self.emb[b])

    def most_common(self, a, n=10, vec=False):
        dd = {key: self.dist(a, val, vec=True) for key, val in self.emb.items()} if vec else {key: self.dist(self.emb[a], val, vec=True) for key, val in self.emb.items()}
        return sorted(dd.items(), key=lambda x: -x[1])[:n]

class TeamEmbedding(object):
    def __init__(self, teams):
        self.emb = teams

    def __getitem__(self, key):
        return self.emb[key]

    def dist(self, a, b, vec=False):
        if vec:
            return 1.0 - distance.cosine(a, b)
        else:
            return 1.0 - distance.cosine(self.emb[a], self.emb[b])

    def most_common(self, a, n=10, vec=False):
        dd = {key: self.dist(a, val, vec=True) for key, val in self.emb.items()} if vec else {key: self.dist(self.emb[a], val, vec=True) for key, val in self.emb.items()}
        return sorted(dd.items(), key=lambda x: -x[1])[:n]

def save(model, emb, team_emb):
    torch.save(model, 'Data/Player2Vec.pth')

    with open('Data/player_emb.pickle', 'wb') as f:
        pickle.dump(emb, f)

    with open('Data/team_emb.pickle', 'wb') as f:
        pickle.dump(team_emb, f)
