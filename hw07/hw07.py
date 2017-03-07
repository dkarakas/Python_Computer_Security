#!/usr/bin/env python

#Homework Number: hw07
#Name: Dimcho Karakashev
#ECN Login: dkarakas
#Due Date: 03/07/17


from BitVector import *
from hashlib import *

K_const = ["428a2f98d728ae22", "7137449123ef65cd", "b5c0fbcfec4d3b2f", "e9b5dba58189dbbc",
     "3956c25bf348b538", "59f111f1b605d019", "923f82a4af194f9b", "ab1c5ed5da6d8118",
     "d807aa98a3030242", "12835b0145706fbe", "243185be4ee4b28c", "550c7dc3d5ffb4e2",
     "72be5d74f27b896f", "80deb1fe3b1696b1", "9bdc06a725c71235", "c19bf174cf692694",
     "e49b69c19ef14ad2", "efbe4786384f25e3", "0fc19dc68b8cd5b5", "240ca1cc77ac9c65",
     "2de92c6f592b0275", "4a7484aa6ea6e483", "5cb0a9dcbd41fbd4", "76f988da831153b5",
     "983e5152ee66dfab", "a831c66d2db43210", "b00327c898fb213f", "bf597fc7beef0ee4",
     "c6e00bf33da88fc2", "d5a79147930aa725", "06ca6351e003826f", "142929670a0e6e70",
     "27b70a8546d22ffc", "2e1b21385c26c926", "4d2c6dfc5ac42aed", "53380d139d95b3df",
     "650a73548baf63de", "766a0abb3c77b2a8", "81c2c92e47edaee6", "92722c851482353b",
     "a2bfe8a14cf10364", "a81a664bbc423001", "c24b8b70d0f89791", "c76c51a30654be30",
     "d192e819d6ef5218", "d69906245565a910", "f40e35855771202a", "106aa07032bbd1b8",
     "19a4c116b8d2d0c8", "1e376c085141ab53", "2748774cdf8eeb99", "34b0bcb5e19b48a8",
     "391c0cb3c5c95a63", "4ed8aa4ae3418acb", "5b9cca4f7763e373", "682e6ff3d6b2b8a3",
     "748f82ee5defb2fc", "78a5636f43172f60", "84c87814a1f0ab72", "8cc702081a6439ec",
     "90befffa23631e28", "a4506cebde82bde9", "bef9a3f7b2c67915", "c67178f2e372532b",
     "ca273eceea26619c", "d186b8c721c0c207", "eada7dd6cde0eb1e", "f57d4f7fee6ed178",
     "06f067aa72176fba", "0a637dc5a2c898a6", "113f9804bef90dae", "1b710b35131c471b",
     "28db77f523047d84", "32caab7b40c72493", "3c9ebe0a15c9bebc", "431d67c49c100d4c",
     "4cc5d4becb3e42b6", "597f299cfc657e2a", "5fcb6fab3ad6faec", "6c44198c4a475817"]


def getWords(read1024bitmessage):
    wordsToReturn = [None] * 80
    #initilize the first 16 values with the original input
    wordsToReturn[0:16] = [read1024bitmessage[i*64:i*64+64] for i in range(0,16)]

    #calculates ther rest of the 80 words used for the rounds
    for i in range(16,80):
         value_to_add = (int(wordsToReturn[i-16]) + int(sigma0(wordsToReturn[i-15])) \
                          +(int(wordsToReturn[i-7])) + int(sigma1(wordsToReturn[i-2]))) % 2**64
         wordsToReturn[i] = BitVector(intVal = value_to_add, size = 64)
    return wordsToReturn

def sigma0(word):
    """Used in generation of the words"""
    word_to_man0 = word.deep_copy()
    word_to_man1 = word.deep_copy()
    word_to_man2 = word.deep_copy()
    return  (word_to_man0 >> 1) ^ (word_to_man1 >> 8) ^ (word_to_man2.shift_right(7))

def sigma1(word):
    """Used in generation of the words"""
    word_to_man0 = word.deep_copy()
    word_to_man1 = word.deep_copy()
    word_to_man2 = word.deep_copy()
    return  (word_to_man0 >> 19) ^ (word_to_man1 >> 61) ^ (word_to_man2.shift_right(6))

def getFileIn1024bits(inputfile):
    """Puts the file into block of 1024 bits"""
    input_text = open(inputfile, 'r+').read()
    num_bytes = len(input_text)#determines the number of bytes in the input file

    list_File_return = []

    bv = BitVector(filename = inputfile)
    while(bv.more_to_read):
        bv_read = bv.read_bits_from_file(1024)
        list_File_return.append(bv_read)

    #Checks in order to detirmine if I have to append one more block for the string length
    if len(list_File_return[-1]) < 895:
        list_File_return[-1] = list_File_return[-1] + BitVector(intVal = 1, size = 1)
        zeros_to_append = 1024 - (len(list_File_return[-1]) + 128)
        list_File_return[-1] = list_File_return[-1] + BitVector(intVal = 0, size = zeros_to_append) \
                                + BitVector(intVal = num_bytes*8, size = 128)
    elif len(list_File_return[-1]) <= 1023:
        list_File_return[-1] = list_File_return[-1] + BitVector(intVal=1, size=1)
        zeros_to_append = 1024 - len(list_File_return[-1])
        list_File_return[-1] = list_File_return[-1] + BitVector(intVal=0, size=zeros_to_append)
        list_File_return.append(BitVector(intVal = num_bytes*8, size = 1024))
    else:
        list_File_return.append(BitVector(intVal = 1, size = 1) + BitVector(intVal = num_bytes*8, size = 1023))

    bv.close_file_object()
    return list_File_return


def hash(inputfile):
    fileIn1024 = getFileIn1024bits(inputfile)
    a = BitVector(hexstring="6a09e667f3bcc908")
    b = BitVector(hexstring="bb67ae8584caa73b")
    c = BitVector(hexstring="3c6ef372fe94f82b")
    d = BitVector(hexstring="a54ff53a5f1d36f1")
    e = BitVector(hexstring="510e527fade682d1")
    f = BitVector(hexstring="9b05688c2b3e6c1f")
    g = BitVector(hexstring="1f83d9abfb41bd6b")
    h = BitVector(hexstring="5be0cd19137e2179")
    for block in fileIn1024:
        wordList = getWords(block)
        a_ini = int(a)
        b_ini = int(b)
        c_ini = int(c)
        d_ini = int(d)
        e_ini = int(e)
        f_ini = int(f)
        g_ini = int(g)
        h_ini = int(h)
        for i in range(80):
            T1 = (int(h) + int(CH(e,f,g)) + int(SUME(e)) + int(wordList[i]) + int(BitVector(hexstring = K_const[i]))) % 2**64
            T2 = (int(SUMA(a)) + int(MAJ(a,b,c))) % 2 ** 64
            h = g
            g = f
            f = e
            e = BitVector(intVal = (int(d) + T1) % (2 ** 64), size = 64)
            d = c
            c = b
            b = a
            a = BitVector(intVal = (T1 + T2)  % 2 ** 64, size = 64)

        a = (int(a) + a_ini) % 2 ** 64
        b = (int(b) + b_ini) % 2 ** 64
        c = (int(c) + c_ini) % 2 ** 64
        d = (int(d) + d_ini) % 2 ** 64
        e = (int(e) + e_ini) % 2 ** 64
        f = (int(f) + f_ini) % 2 ** 64
        g = (int(g) + g_ini) % 2 ** 64
        h = (int(h) + h_ini) % 2 ** 64
        a = BitVector(intVal=a, size=64)
        b = BitVector(intVal=b, size=64)
        c = BitVector(intVal=c, size=64)
        d = BitVector(intVal=d, size=64)
        e = BitVector(intVal=e, size=64)
        f = BitVector(intVal=f, size=64)
        g = BitVector(intVal=g, size=64)
        h = BitVector(intVal=h, size=64)
    return a + b + c + d + e + f + g + h

def CH(e,f,g):
    e_copy = e.deep_copy()
    f_copy = f.deep_copy()
    g_copy = g.deep_copy()
    return (e_copy & f_copy) ^ (~e_copy & g_copy)

def MAJ(a,b,c):
    a_copy = a.deep_copy()
    b_copy = b.deep_copy()
    c_copy = c.deep_copy()
    return (a_copy & b_copy) ^ (a_copy & c_copy) ^ (b_copy & c_copy)

def SUMA(a):
    a_copy = a.deep_copy()
    a_copy1 = a.deep_copy()
    a_copy2 = a.deep_copy()
    return (a_copy >> 28) ^ (a_copy1 >> 34) ^ (a_copy2 >> 39)

def SUME(e):
    e_copy = e.deep_copy()
    e_copy1 = e.deep_copy()
    e_copy2 = e.deep_copy()
    return (e_copy >> 14) ^ (e_copy1 >> 18) ^ (e_copy2 >> 41)

if __name__ == "__main__":
    hash_val = hash("Input.txt")


    with open ("output.txt", 'w') as MyFile:
        MyFile.write(hash_val.get_hex_string_from_bitvector())

    with open("Input.txt", "rb") as testHash:
        file = testHash.read()

    if hash_val.get_hex_string_from_bitvector() == sha512(file).hexdigest():
        print("Correct hash!")