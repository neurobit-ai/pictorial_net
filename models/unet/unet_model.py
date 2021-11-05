""" Full assembly of the parts to form the complete network """

import torch.nn.functional as F

from .unet_parts import *


# 1x1 convolution
def conv1x1(in_channels, out_channels, stride=1):
    return nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, padding=0, bias=False)



class UNet(nn.Module):
    def __init__(self, in_channels, out_channels, bilinear=True):
        super(UNet, self).__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.bilinear = bilinear
        
        num = 64
        self.inc = DoubleConv(in_channels, num)
        self.down1 = Down(num, num*2)
        self.down2 = Down(num*2 , num*4)
        self.down3 = Down(num*4 , num*8)
        factor = 2 if bilinear else 1
        self.down4 = Down(num*8 , num*16 // factor)
        self.up1 = Up(num*16 , num*8 // factor, bilinear)
        self.up2 = Up(num*8 , num*4 // factor, bilinear)
        self.up3 = Up(num*4 , num*2 // factor, bilinear)
        self.up4 = Up(num*2 , num, bilinear)
        
        self.conv1x1 = conv1x1()

    def forward(self, x):
        x1 = self.inc(x)
        x2 = self.down1(x1)
        x3 = self.down2(x2)
        x4 = self.down3(x3)
        x5 = self.down4(x4)
        x = self.up1(x5, x4)
        x = self.up2(x, x3)
        x = self.up3(x, x2)
        x = self.up4(x, x1)
        gazemap = 

        return x, gazemap
