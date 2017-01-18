#! /usr/bin/env python

import sys

#reading key file
KEY_FILE = open("key.txt",'r')          #opening a file containing the key
PLAIN_TEXT = open("input.txt",'r')      #opening a file containing the plain text

key = KEY_FILE.read()                   #reading the whole key value
key_len = len(key)                      #gets the length of the key
curIndexKey = 0                         #initialize the key index to encrypt

while True:
    chIn = PLAIN_TEXT.read(1)           #reading one char at a time

    if not chIn:                        #checks if we had reached the end of the file
        break

    if(curIndexKey >= curIndexKey):
        curIndexKey = 0
"""
for inputa in read:
    print(inputa+ "\n" )
"""

