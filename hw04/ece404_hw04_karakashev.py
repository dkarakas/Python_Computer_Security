#!/usr/bin/env python
"""AES ENCRYPTION DECRYPTION ALGO"""

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
    word_into_bytes = []
    for i in range(4):
        word_into_bytes.append(wordToSubBytes[i * 8:i * 8 + 8])
    if enc_dec == "e":
        c = BitVector(bitstring='01100011')
        for num_byte, byte in enumerate(word_into_bytes):
            # print(str(num_byte)  + " " + str(byte))
            byte_mi = byte.gf_MI(BitVector(bitstring='100011011'), 8)
            b1, b2, b3, b4 = [byte_mi.deep_copy() for x in range(4)]
            byte_mi ^= (b1 >> 4) ^ (b2 >> 5) ^ (b3 >> 6) ^ (b4 >> 7) ^ c
            wordToSubBytes[num_byte * 8:num_byte * 8 + 8] = byte_mi
    else:
        d = BitVector(bitstring='00000101')
        for num_byte, byte in enumerate(word_into_bytes):
            # print(str(num_byte)  + " " + str(byte))
            byte_mi = byte.gf_MI(BitVector(bitstring='100011011'), 8)
            b1, b2, b3, b4 = [byte_mi.deep_copy() for x in range(4)]
            byte_mi ^= (b1 >> 2) ^ (b2 >> 5) ^ (b4 >> 7) ^ d
            wordToSubBytes[num_byte * 8:num_byte * 8 + 8] = byte_mi
    return wordToSubBytes


def gee(word_to_gee_2, round_constant):
    word_to_gee = word_to_gee_2.deep_copy()
    word_to_gee << 8
    # SubBytes
    word_to_gee = subBytes(word_to_gee, "e")
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


def encrypt(bv,fileOut,keys):

    while bv.more_to_read:
        bitvec = bv.read_bits_from_file( 128 )
        size = bitvec.length()
        ##Xor with the 4 words of the key schedule
        if size > 0:
            if size < 128:
                bitvec.pad_from_right(128 - size)
            ##EACH ROUND
            ##SubBytes
            ##ShiftRows
            ##MixColumns
            ##AddKeys

        bitvec.write_to_file(fileOut)



def decrypt(bv,fileOut,keys):
    while bv.more_to_read:
        print("ceh")
        bitvec = bv.read_bits_from_file( 128 )
        size = bitvec.length()
        ##Xor the cypher with last 4 words
        if size > 0:
            if size < 128:
                bitvec.pad_from_right(128 - size)
                ##Inverse shift rows
                ##Inverse sub bytes
                ##Add round keys
                ##Inverse mix colums

        bitvec.write_to_file(fileOut)





def AES_algo():
    keys = key_schedule()

    try:
        fileOutputEncr = open('encrypted.txt', 'wb')
    except:
        print("Error opening encrypted.txt")
        sys.exit(1)
    bvPlainFile = BitVector(filename='plaintext.txt')

    encrypt(bvPlainFile,fileOutputEncr,keys)

    try:
        fileOutputDecr = open('decrypted.txt', 'wb')
    except:
        print("Error opening encrypted.txt")
        sys.exit(1)
    bvEncrFile = BitVector(filename='encrypted.txt')
    decrypt(bvEncrFile,fileOutputDecr,keys)

if __name__ == "__main__":
    AES_algo()
