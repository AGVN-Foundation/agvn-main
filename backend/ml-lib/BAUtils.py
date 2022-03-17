#!/usr/bin/env python3

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms

def transform(mode):
    if mode == 'train':
        return transforms.Compose([transforms.Resize((72, 48)),transforms.ToTensor()])
    elif mode == 'test':
        return transforms.Compose([transforms.Resize((72, 48)),transforms.ToTensor()])

class Network(nn.Module):
    def __init__(self): 
        super().__init__()
        
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3)
        self.bn1 = nn.BatchNorm2d(64)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        self.conv2_x1 = nn.Sequential(
            nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64)
        )

        self.conv2_x2 = nn.Sequential(
            nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64)
        )

        self.conv2_x3 = nn.Sequential(
            nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64)
        )

        self.conv3_x1 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128)
        )

        self.downsample1 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(128)
        )

        self.conv3_x2 = nn.Sequential(
            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128)
        )

        self.conv3_x3 = nn.Sequential(
            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128)
        )

        self.conv3_x4 = nn.Sequential(
            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128)
        )

        self.conv4_x1 = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256)
        )

        self.downsample2 = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(256)
        )

        self.conv4_x2 = nn.Sequential(
            nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256)
        )

        self.conv4_x3 = nn.Sequential(
            nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256)
        )

        self.conv4_x4 = nn.Sequential(
            nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256)
        )

        self.conv4_x5 = nn.Sequential(
            nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256)
        )

        self.conv4_x6 = nn.Sequential(
            nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256)
        )

        self.conv5_x1 = nn.Sequential(
            nn.Conv2d(256, 512, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(512)
        )

        self.downsample3 = nn.Sequential(
            nn.Conv2d(256, 512, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(512)
        )

        self.conv5_x2 = nn.Sequential(
            nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(512)
        )

        self.conv5_x3 = nn.Sequential(
            nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(512)
        )


        self.relu = nn.ReLU()
        self.avgpool = nn.AdaptiveAvgPool2d((1,1))
        self.fc = nn.Linear(512, 10)
        self.soft_max = nn.Softmax(dim=1)

    def forward(self, t):
        t = self.conv1(t) # 3*64*64 -> 64*32*32
        t = self.bn1(t)
        t = self.relu(t)
        t = self.maxpool(t) # 64*32*32 -> 64*16*16

        # 1st resblock

        identity = t.clone()

        t = self.conv2_x1(t) 
        t = self.relu(t + identity)

        identity = t.clone()

        t = self.conv2_x2(t) 
        t = self.relu(t + identity)

        identity = t.clone()

        t = self.conv2_x3(t) 
        t = self.relu(t + identity)

        # 2nd resblock
        identity = t.clone()
        identity = self.downsample1(identity)

        t = self.conv3_x1(t) # 64*16*16 -> 128*8*8
        t = self.relu(t + identity)
        
        identity = t.clone()

        t = self.conv3_x2(t)
        t = self.relu(t + identity)

        identity = t.clone()

        t = self.conv3_x3(t)
        t = self.relu(t + identity)

        identity = t.clone()

        t = self.conv3_x4(t)
        t = self.relu(t + identity) 

        # 3rd resblock

        identity = t.clone()
        identity = self.downsample2(identity)

        t = self.conv4_x1(t) # 128*8*8 -> 256*4*4
        t = self.relu(t + identity)
        
        identity = t.clone()

        t = self.conv4_x2(t)
        t = self.relu(t + identity)

        identity = t.clone()

        t = self.conv4_x3(t)
        t = self.relu(t + identity)

        identity = t.clone()

        t = self.conv4_x4(t)
        t = self.relu(t + identity)

        identity = t.clone()

        t = self.conv4_x5(t)
        t = self.relu(t + identity)

        identity = t.clone()

        t = self.conv4_x6(t)
        t = self.relu(t + identity)

        # 4th resblock

        identity = t.clone()
        identity = self.downsample3(identity)

        t = self.conv5_x1(t) # 256*4*4 -> 512*2*2
        t = self.relu(t + identity)
        
        identity = t.clone()

        t = self.conv5_x2(t)
        t = self.relu(t + identity)
        
        identity = t.clone()

        t = self.conv5_x3(t)
        t = self.relu(t + identity)
        
        # average pooling
        t = self.avgpool(t)

        # final connected layer
        t = t.reshape(t.shape[0], -1)
        t = self.fc(t)

        # softmax
        t = self.soft_max(t)

        return t

net = Network()
lossFunc = nn.CrossEntropyLoss()
dataset = "./images"
train_val_split = 0.90
batch_size = 100
epochs = 30
optimiser = optim.Adam(net.parameters(), lr=0.001)
