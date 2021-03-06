import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.models as models

from .basic_model import BasicModel

class identity(nn.Module):
    def __init__(self):
        super(identity, self).__init__()
    
    def forward(self, x):
        return x

class mlp_module(nn.Module):
    def __init__(self):
        super(mlp_module, self).__init__()
        self.fc1 = nn.Linear(512, 512)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(512, 8)
        self.dropout = nn.Dropout(0.5)
        
    def forward(self, x):
        x = self.relu1(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

class Resnet34_MLP(BasicModel):
    def __init__(self, args):
        super(Resnet34_MLP, self).__init__(args)
        self.resnet34 = models.resnet34(pretrained=False)
        self.resnet34.conv1 = nn.Conv2d(16, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.resnet34.fc = identity()
        self.mlp = mlp_module()
        self.optimizer = optim.Adam(self.parameters(), lr=args.lr, betas=(args.beta1, args.beta2), eps=args.epsilon)

    def compute_loss(self, output, target, _):
        pred = output[0]
        loss = F.cross_entropy(pred, target)
        return loss

    def forward(self, x):
        features = self.resnet34(x.view(-1, 16, 224, 224))
        score = self.mlp(features)
        return score, None

    