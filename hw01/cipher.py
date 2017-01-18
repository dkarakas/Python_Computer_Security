#! /usr/bin/env python

import sys

#reading key file
KEY_FILE = open("key.txt",'r')          #opening a file containing the key
PLAIN_TEXT = open("input.txt",'r')      #opening a file containing the plain text
OUTPUT_TEXT = open("write.txt",'w')     #opening a file to save the encryption

key = KEY_FILE.read()                   #reading the whole key value
key_len = len(key) - 1                  #gets the length of the key & - 1 to get rid of the new line
curIndexKey = 0                         #initialize the key index to encrypt


while True:
    chIn = PLAIN_TEXT.read(1)           #reading one char at a time
    if( not chIn ) or ( chIn == '\n' ):    #checks if we had reached the end of the file
        break
    if( curIndexKey >= key_len):
        curIndexKey = 0
    pos_to_move = abs(ord('A') - ord(key[curIndexKey]))     #computing how much should i move the encryption key
    curIndexKey += 1                    #moving through the key
    encryptCh = ord(chIn) + pos_to_move
    if( encryptCh > 122):
        encryptCh = ( encrypthCh - 122 ) + 65
    if ( encrypthCh > 90 ) and ( encrypthCh < 97 ):
        encryptCh = encryptCh + 6
    OUTPUT_TEXT.write(char(encryptCh)

    #sys.stdout.write(str(pos_to_move) + ' '+ chIn + ' ' + key[curIndexKey] + ' ')
    #print curIndexKey

KEY_TEXT.close()
PLAIN_TEXT.close()
OUTPUT_TEXT.close()
