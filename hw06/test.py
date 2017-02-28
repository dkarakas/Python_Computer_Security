#!/usr/bin/env/python
import sys
import pprint
import argparse
from PrimeGenerator import *
from BitVector import *
from solve_pRoot import *


def arg_setup():
    # takes care of arguments in command line
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile')
    parser.add_argument('outputfile')
    args = parser.parse_args()
    return args


def arg_setup():
    # takes care of arguments in command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', action='store_true')
    parser.add_argument('-e', action='store_true')
    parser.add_argument('inputfile')
    parser.add_argument('outputfile')
    args = parser.parse_args()
    return args


def create_keys():
    # creates the keys
    with open('private_key.txt', 'r') as f:
        d = f.readline()
        n = f.readline()
        p = f.readline()
        q = f.readline()
    d = BitVector(intVal=int(d))
    n = BitVector(intVal=int(n))
    p = BitVector(intVal=int(p))
    q = BitVector(intVal=int(q))
    with open('public_key.txt', 'r') as f:
        e = f.readline()
        n = f.readline()
    e = BitVector(intVal=int(e))
    n = BitVector(intVal=int(n))
    priv = (d, n, p, q)
    pub = (e, n)
    return (pub, priv)


def find_exponent(block, d, pq):
    res = 1
    while (d > 0):
        if (d & 1):
            res = (res * block) % pq
        d = d >> 1
        block = (block * block) % pq
    return res


def Chinese_magic(blok, d, n, p, q):
    Vq = find_exponent(int(blok), int(d), int(q))
    Vp = find_exponent(int(blok), int(d), int(p))
    n1 = int(n) / int(p)
    n2 = int(n) / int(q)

    n1_bv = BitVector(intVal=n1)
    n2_bv = BitVector(intVal=n2)

    n1_MI = int(n1_bv.multiplicative_inverse(p))
    n2_MI = int(n2_bv.multiplicative_inverse(q))

    Xp = int(q) * n1_MI
    Xq = int(p) * n2_MI
    magic_num = ((Vp * Xp) + (Vq * Xq)) % int(n)

    return magic_num


def decrypt(input_file, output_file, key):
    d = key[0]
    FILEOUT = open(output_file, 'ab')
    n = key[1]
    p = key[2]
    q = key[3]
    result_bv = BitVector(size=0)  # used to append the results
    bv = BitVector(filename=input_file)
    while (bv.more_to_read):
        bitvec = bv.read_bits_from_file(256)
        dec = Chinese_magic(bitvec, d, n, p, q)
        pad = 128 - BitVector(intVal=dec).length()
        result_bv += BitVector(intVal=dec, size=128)

    result_bv.write_to_file(FILEOUT)


def encrypt(input_file, output_file, key):
    e = key[0]
    FILEOUT = open(output_file, 'a')
    n = key[1]
    result_bv = BitVector(size=0)  # used to append the results
    bv = BitVector(filename=input_file)
    while (bv.more_to_read):
        bitvec = bv.read_bits_from_file(128)
        leng = bitvec.length()
        pad = 128 - leng
        bitvec.pad_from_right(pad)
        bitvec.pad_from_left(128)

        temp = find_exponent(int(bitvec), int(e), int(n))
        temp = BitVector(intVal=temp)
        pad = 256 - temp.length()
        temp.pad_from_left(pad)
        result_bv += temp
    result_bv.write_to_file(FILEOUT)


def create_keys():
    # creates the keys
    e = BitVector(intVal=3)
    uno = BitVector(intVal=1)
    tres = BitVector(intVal=3)  # used for checking the last two bits
    generator = PrimeGenerator(bits=128, debug=0)
    p = BitVector(intVal=generator.findPrime())
    while (p[0:2] != tres and int(e.gcd(BitVector(intVal=int(p) - 1))) != 1):
        p = BitVector(intVal=generator.findPrime())
    q = BitVector(intVal=generator.findPrime())
    while (q[0:2] != tres and int(e.gcd(BitVector(intVal=int(q) - 1))) != 1 and p != q):
        q = BitVector(intVal=generator.findPrime())
    n = int(p) * int(q)
    n = BitVector(intVal=n)
    to = BitVector(intVal=((int(p) - 1) * (int(q) - 1)))
    d = e.multiplicative_inverse(to)
    priv = (d, n, p, q)
    pub = (e, n)
    return (pub, priv)


# takes 3 keys as tuples of two BitVectors and the filenames of the encrypted texts
# assumes 3 keys have same e values since it is one of the conditions for this algorithm to work

def Crack_RSA(key1, key2, key3, etext1, etext2, etext3, output_file):
    fin = BitVector(size=0)
    e = key1[0]
    FILEOUT = open(output_file, 'a')
    n1 = key1[1]

    n2 = key2[1]

    n3 = key3[1]
    bigN = int(n1) * int(n2) * int(n3)
    bigN1 = BitVector(intVal=(bigN / int(n1)))
    bigN2 = BitVector(intVal=(bigN / int(n2)))
    bigN3 = BitVector(intVal=(bigN / int(n3)))
    mi1 = int(bigN1.multiplicative_inverse(n1))
    mi2 = int(bigN2.multiplicative_inverse(n2))
    mi3 = int(bigN3.multiplicative_inverse(n3))

    bv1 = BitVector(filename=etext1)
    bv2 = BitVector(filename=etext2)
    bv3 = BitVector(filename=etext3)

    while (bv1.more_to_read):
        bitvec1 = bv1.read_bits_from_file(256)
        bitvec2 = bv2.read_bits_from_file(256)
        bitvec3 = bv3.read_bits_from_file(256)

        temp = ((int(bitvec1) * int(bigN1) * mi1) +
                (int(bitvec2) * int(bigN2) * mi2) +
                (int(bitvec3) * int(bigN3) * mi3)) % bigN

        temp2 = solve_pRoot(3, temp)
        temp = BitVector(intVal=temp2)
        pad = 128 - temp.length()
        temp.pad_from_left(pad)
        fin += temp
    fin.write_to_file(FILEOUT)
    return


if __name__ == "__main__":
    pub1, priv1 = create_keys()
    pub2, priv2 = create_keys()
    pub3, priv3 = create_keys()
    encrypt("message.txt", "encry1.txt", pub1)
    encrypt("message.txt", "encry2.txt", pub2)
    encrypt("message.txt", "encry3.txt", pub3)
    Crack_RSA(pub1, pub2, pub3, "encry1.txt", "encry2.txt", "encry3.txt", argu.outputfile)