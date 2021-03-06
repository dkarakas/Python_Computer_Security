#!/usr/bin/env python
"""AES ENCRYPTION DECRYPTION ALGO"""

#Homework Number:hw04
#Name:Dimcho karakashev
#ECN Login: dkarakas
#Due Date: 02/10/17

from BitVector import *

modulous = BitVector(bitstring="100011011")


def ask_user_for_key():
    key = input("Enter key:")
    key = key.strip()
    key = key[0:16]  # takes care of longer keys than 16 bytes
    key += '0' * (16 - len(key))  # takes care of smaller length keys
    key_bv = BitVector(textstring=key)
    return key_bv


def loadFile(nameOfFile):
    with open(nameOfFile, "r") as fileInput:
        rtn_file = fileInput.read().replace('\n', '')
    return rtn_file


def subBytes(wordToSubBytes, enc_dec):
    """word_to_gee_2 needs to be 32 bit"""
    word_into_bytes = []
    for i in range(4):
        word_into_bytes.append(wordToSubBytes[i * 8:i * 8 + 8])
    if enc_dec == "e":
        c = BitVector(bitstring='01100011')
        for num_byte, byte in enumerate(word_into_bytes):
            # print(str(num_byte)  + " " + str(byte))
            #print(byte_mi)
            if byte != BitVector(bitstring='00000000'):
                byte_mi = byte.gf_MI(BitVector(bitstring='100011011'), 8)
            else:
                byte_mi = byte
            b1, b2, b3, b4 = [byte_mi.deep_copy() for x in range(4)]
            byte_mi ^= (b1 >> 4) ^ (b2 >> 5) ^ (b3 >> 6) ^ (b4 >> 7) ^ c
            wordToSubBytes[num_byte * 8:num_byte * 8 + 8] = byte_mi
    else:
        d = BitVector(bitstring='00000101')
        for num_byte, byte in enumerate(word_into_bytes):
            # print(str(num_byte)  + " " + str(byte))
            if byte != BitVector(bitstring='00000000'):
                byte_mi = byte.gf_MI(BitVector(bitstring='100011011'), 8)
            else:
                byte_mi = byte
            b1, b2, b3, b4 = [byte_mi.deep_copy() for x in range(4)]
            byte_mi ^= (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
            wordToSubBytes[num_byte * 8:num_byte * 8 + 8] = byte_mi
    return wordToSubBytes


def gee(word_to_gee_2, round_constant):
    word_to_gee = word_to_gee_2.deep_copy()
    word_to_gee << 8
    # SubBytes
    word_to_gee = subBytes(word_to_gee, "e")
    word_to_gee[0:8] ^= round_constant
    return word_to_gee  # before returning I xor the bits with the round constant

def gen_round_const():
    list_round_const = []
    list_round_const.append(BitVector(intVal=0x01, size=8))
    for i in range(1, 10):
        list_round_const.append(list_round_const[i - 1].gf_multiply_modular(BitVector(intVal=0x02), modulous, 8))
    return list_round_const


def key_schedule():
    key_bv = ask_user_for_key()
    list_round_const = gen_round_const()

    key_list_words = [BitVector(textstring="0") for i in range(44)]  # arrenging the input into words [w0,w1,w2,w3]
    for i in range(4):
        key_list_words[i] = key_bv[i * 32:i * 32 + 32]  # put the key in the first 4 words

    for i in range(4, 44):
        if i % 4 == 0:
            key_list_words[i] = key_list_words[i - 4] ^ gee(key_list_words[i - 1], list_round_const[int(i / 4 - 1)])
        else:
            key_list_words[i] = key_list_words[i - 1] ^ key_list_words[i - 4]
    return key_list_words

def shift(l, n):
    return l[n:] + l[:n]

def shiftRows(bitVec, dec_or_enc):
    matrix = [[0 for i in range(4)] for i in range(4)]
    for i in range(4):
        for y in range(4):
            matrix[y][i] = bitVec[i*32+y*8:i*32+y*8+8]

    if dec_or_enc == "e":
        for i in range(1,4):
            shift(matrix[i],i)
    else:
        for i in range(1,4):
            shift(matrix[i],-i)

    for i in range(4):
        for y in range(4):
            bitVec[i*32+y*8:i*32+y*8+8] = matrix[y][i]
    return  bitVec

def mixColumns(bitVec, dec_or_enc):
    matrix = [[0 for i in range(4)] for i in range(4)]
    for i in range(4):
        for y in range(4):
            matrix[y][i] = bitVec[i*32+y*8:i*32+y*8+8]

    if dec_or_enc == "e":
        for row in [x * 32 for x in range(0, 4)]:
            for colm in range(4):
                bitVec[(colm * 8 + row) % 128:((colm * 8 + row +8)) % 129] = bitVec[(colm * 8 + row) % 128:((colm * 8 + row +8)) % 129].gf_multiply_modular(BitVector( intVal=0x02, size=8),modulous,8) \
                            ^ bitVec[((colm + 1) * 8 + row) % 128:(((colm + 1) * 8 + row + 8)) % 129].gf_multiply_modular(BitVector( intVal=0x03, size=8),modulous,8) \
                            ^ bitVec[((colm + 2) * 8 + row) % 128:(((colm + 2) * 8 + row + 8)) % 129] \
                            ^ bitVec[(((colm + 3) * 8 + row) % 128):((((colm + 3) * 8 + row +8)) % 129)]
    else:
        for row in [x * 32 for x in range(0, 4)]:
            for colm in range(4):
                bitVec[(colm * 8 + row) % 128:((colm * 8 + row +8)) % 129] = bitVec[(colm * 8 + row) % 129:((colm * 8 + row +8)) % 129].gf_multiply_modular(BitVector( intVal=0x0E, size=32),modulous,8) \
                                        ^ bitVec[((colm + 1) * 8 + row) % 128:(((colm + 1) * 8 + row + 8)) % 129].gf_multiply_modular(BitVector(intVal=0x0B, size=8),modulous,8) \
                                        ^ bitVec[((colm + 2) * 8 + row) % 128:(((colm + 2) * 8 + row + 8)) % 129].gf_multiply_modular(BitVector(intVal=0x0D, size=8),modulous,8) \
                                        ^ bitVec[(((colm + 3) * 8 + row) % 128):((((colm + 3) * 8 + row +8)) % 129)].gf_multiply_modular(BitVector(intVal=0x09, size=8),modulous,8)

    for i in range(4):
        for y in range(4):
            bitVec[i*32+y*8:i*32+y*8+8] = matrix[y][i]
    return  bitVec

def encrypt(bv,fileOut,keys):
    cur = 0
    while bv.more_to_read:
        bitvec = bv.read_bits_from_file( 128 )
        print("Len :" + str(cur))
        size = bitvec.length()
        ##Xor with the 4 words of the key schedule
        for i in range(4):
            bitvec ^= keys[i]
        if size > 0:
            if size < 128:
                bitvec.pad_from_right(128 - size)
            ##EACH ROUND
            for i in range(1,11):
                ##SubBytes
                for i in range(4):
                    bitvec[i * 32:i * 32 + 32] = subBytes(bitvec[i * 32:i * 32 + 32],"e")  # put the key in the first 4 words
                ##ShiftRows
                shiftRows(bitvec,"e")
                ##MixColumns
                mixColumns(bitvec,"e")
                ##AddKeys
                bitvec ^= keys[i*4] ^ keys[i*4 + 1] ^ keys[i*4 + 2] ^ keys[i*4 + 3]
        hexStrToOutput = bitvec.get_bitvector_in_hex()
        fileOut.write(hexStrToOutput)
        cur += 16


def decrypt(encrypted_str,fileOut,keys):
    cur = 0
    assert(len(encrypted_str) % 32 == 0), "Not encrypted right! Missing chars!"
    for i in range(int(len(encrypted_str)/32)):
        bitvec = BitVector(hexstring = encrypted_str[i*32: i*32 + 32])
        print("Len :" + str(cur))
        size = bitvec.length()
        ##Xor the cypher with last 4 words
        for i in reversed(range(40,44)):
            bitvec ^= keys[i]
        if size > 0:
            if size < 128:
                bitvec.pad_from_right(128  - size)
            for i in reversed(range(0, 10)):
                ##ShiftRowss
                shiftRows(bitvec, "d")
                ##Inverse sub bytes
                for i in range(4):
                    bitvec[i * 32:i * 32 + 32] = subBytes(bitvec[i * 32:i * 32 + 32],"d")  # put the key in the first 4 words
                ##Add round keys
                bitvec ^= keys[i*4] ^ keys[i*4 + 1] ^ keys[i*4 + 2] ^ keys[i*4 + 3]
                ##Inverse mix colums
                mixColumns(bitvec, "d")

        bitvec.write_to_file(fileOut)
        cur += 16






def AES_algo():
    keys = key_schedule()

    try:
        fileOutputEncr = open('encrypted.txt', 'w')
    except:
        print("Error opening encrypted.txt")
        sys.exit(1)
    bvPlainFile = BitVector(filename='plaintext.txt')

    encrypt(bvPlainFile,fileOutputEncr,keys)

    bvPlainFile.close_file_object()
    fileOutputEncr.close()

    try:
        fileOutputDecr = open('decrypted.txt', 'wb')
    except:
        print("Error opening encrypted.txt")
        sys.exit(1)
    encrypted_str = loadFile('encrypted.txt')

    decrypt(encrypted_str,fileOutputDecr,keys)

    fileOutputDecr.close()

if __name__ == "__main__":
    AES_algo()
