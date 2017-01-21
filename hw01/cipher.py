#! /usr/bin/env python

#Dimcho Karakashev
#01/18/17
#ece404 hw01
#assumption that the only input includes A-Z and a-z. Same applys for the key

import sys

#reading key file
KEY_FILE = open("key.txt",'r')          #opening a file containing the key
PLAIN_TEXT = open("input.txt",'r')      #opening a file containing the plain text
OUTPUT_TEXT = open("output.txt",'w')     #opening a file to save the encryption

key = KEY_FILE.read()                   #reading the whole key value
key_len = len(key) - 2                  #gets the length of the key & - 1 to get rid of the new line
curIndexKey = 0                         #initialize the key index to encrypt


while True:
    chIn = PLAIN_TEXT.read(1)           #reading one char at a time
    if( not chIn ) or ( chIn == '\n' ): #checks if we had reached the end of the file
        break
    if( curIndexKey > key_len):         #interating through the key in the file
        curIndexKey = 0 
    
    #computing how much should i move the encryption key
    if( (ord(key[curIndexKey]) > 64) and (ord(key[curIndexKey]) < 91) ):    #if it is uppercase
        pos_to_move = abs(ord('A') - ord(key[curIndexKey]))
    elif( (ord(key[curIndexKey]) > 96) and (ord(key[curIndexKey]) < 173) ): #if it is lowercase
        pos_to_move = abs(ord('A') - ord(key[curIndexKey]) + 6)

    encryptCh = ord(chIn) + pos_to_move

    if( encryptCh > 122 ):                              #dealing with the values higher than the highest lower case char
        encryptCh = encryptCh - 58 
    if( ( encryptCh > 90 ) and ( encryptCh < 97 ) ):    #taking care of the values between upper and lower case
        encryptCh = encryptCh + 6

    OUTPUT_TEXT.write(chr(encryptCh))

    #debugging statement
    #print("input: " + chIn  + " "\
    #        "key: " + key[curIndexKey] + " " + \
    #        str(pos_to_move) + "Encrypted char: " + chr(encryptCh) + " " + str(encryptCh))
    curIndexKey += 1                    #moving through the key

#Closing files
KEY_FILE.close()
PLAIN_TEXT.close()
OUTPUT_TEXT.close()
