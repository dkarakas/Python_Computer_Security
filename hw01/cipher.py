#! /usr/bin/env python

#reading key file
KEY_FILE = open("key.txt",'r')          #opening a file containing the key
PLAIN_TEXT = open("input.txt",'r')      #opening a file containing the plain text

key = KEY_FILE.read();                  #reading the whole key value

while True:
    chIn = PLAIN_TEXT.read(1);          #reading one char at a time

"""
for inputa in read:
    print(inputa+ "\n" )
"""

