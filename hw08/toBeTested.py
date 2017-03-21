#!/usr/bin/env python

from Karakashev_hw08 import *

spoofIP='';
targetIP='';
rangeStart=0;#number
rangeEnd=0;#number
port=0;#number
Tcp = TcpAttack(spoofIP,targetIP)
TcpAttack.scanTarge(rangeStart,rangeEnd)
if (Tcp.attackTarget(port)):
    print("Por was open to attacks")