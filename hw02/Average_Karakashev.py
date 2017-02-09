#!/usr/bin/env python

## Dimcho Karakashev
## Average_karakashev.py

import sys
from BitVector import *
'''
Output of the script:
Number of different bits between original and one bit change in the plain text is 30
Number of different bits between original and one bit change in the plain text is 26
Number of different bits between original and one bit change in the plain text is 30
On average difference is 28.67
Number of different bits between original and encryption with 1 bit change in encryption key is 4300
Number of different bits between original and encryption with 1 bit change in encryption key is 4237
Number of different bits between original and encryption with 1 bit change in encryption key is 4370
On average difference with change of encryption key is 4302.33
Number of different bits between original and s table change is 28
'''

def open_files():
    try:
        file_1 = BitVector(filename='encrypted_1.txt')
        file_2 = BitVector(filename='encrypted_2.txt')
        file_3 = BitVector(filename='encrypted_3.txt')
        file_4 = BitVector(filename='encryption_1.txt')
        file_5 = BitVector(filename='encryption_2.txt')
        file_6 = BitVector(filename='encryption_3.txt')
        file_7 = BitVector(filename='s_table1_1.txt')
    except:
        print("error opening some of the files")
        sys.exit(1)
    list_files = [file_1, file_2, file_3, file_4, file_5, file_6, file_7]
    return list_files


def compare(file, name, option):
    global total_bits
    try:
        if option == 1:
            orig = BitVector(filename='encrypted.txt')
        else:
            orig = BitVector(filename='s_table1.txt')
    except:
        print("error opening the original file")
        sys.exit(1)

    diff = 0  # number of different bits
    while orig.more_to_read:
        orig_bits = orig.read_bits_from_file(64)
        if orig_bits.length():
            orig_bits.pad_from_right(64 - orig_bits.length())
        chan_bits = file.read_bits_from_file(64)
        if chan_bits.length():
            chan_bits.pad_from_right(64 - chan_bits.length())

        for i in range(64):
            if orig_bits[i] != chan_bits[i]:
                diff = diff + 1

    print("Number of different bits between original and {1} is {0}".format(diff, name))
    total_bits = total_bits + diff
    orig.close_file_object()

total_bits=0
list_of_files = open_files()
compare(list_of_files[0], "one bit change in the plain text",1)
compare(list_of_files[1], "one bit change in the plain text",1)
compare(list_of_files[2], "one bit change in the plain text",1)
temp_bits=total_bits
print("On average difference is {0}".format(round(total_bits/3,2)))
compare(list_of_files[3], "encryption with 1 bit change in encryption key",1)
compare(list_of_files[4], "encryption with 1 bit change in encryption key",1)
compare(list_of_files[5], "encryption with 1 bit change in encryption key",1)
print("On average difference with change of encryption key is {0}".format(round((total_bits-temp_bits)/3,2)))
total_bits=0
compare(list_of_files[6], "s table change",2)

sys.exit(0)