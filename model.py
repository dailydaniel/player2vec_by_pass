#!/usr/bin/python
# -*- coding: UTF-8 -*-

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import numpy as np

from tqdm import tqdm

class Pass2Vec(nn.Module):

    def __init__(self, embedding_dim, input_size, vocabulary_size):
        super(Pass2Vec, self).__init__()

        self.fc1 = nn.Linear(input_size, embedding_dim)

        self.fc2 = nn.Linear(embedding_dim, vocabulary_size)

    def forward(self, x):
        z1 = self.fc1(x)
        z2 = self.fc2(z1)
        return z2

def train(model, data, players, player2idx, loss_function, num_epoch=50):
    avg_loss = []

    for epoch in range(num_epoch): # tqdm(range(200)):

        running_loss = []
        for i in range(data.index.size-1):
            batch = torch.tensor(data[i:i+1].values.astype('float64')).type('torch.FloatTensor')
            targets = torch.tensor([player2idx[players[i:i+1].values[0][0]]]).type('torch.LongTensor')

            model.zero_grad()

            tag_scores = model(batch)

            loss = loss_function(tag_scores, targets)
            loss.backward()
            optimizer.step()

            for p in model.parameters(): # making weights non-negative
                p.data.clamp_(0)

            running_loss.append(loss.item())

        avg_loss.append(round(sum(running_loss) / len(running_loss), 4))
        print('epo: {0}, loss: {1}'.format(epoch, avg_loss[-1]))
    return model, avg_loss
