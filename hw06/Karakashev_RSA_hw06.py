#!/usr/bin/env python

from PrimeGenerator import PrimeGenerator
from BitVector import *

#Homework Number: hw06
#Name: Dimcho Karakashev
#ECN Login: dkarakas
#Due Date: 02/23/17


#As specified by the assignment
E_KEY = 65537

def gcd(a,b):
    while b:
        a,b = b, a % b
    return a

def genPrimes():
    generator = PrimeGenerator(bits=128)
    while (1):
        p, q = generator.findPrime(), generator.findPrime()
        if not ((p & (1 << 127)) | (p & (1 << 126)) | (p & 1)):  ##check if appropriate bits are not set
            continue
        if not ((q & (1 << 127)) | (q & (1 << 126)) | (q & 1)):  ##check if appropriate bits are not set
            continue
        if p == q:
            continue
        if (gcd(p-1,E_KEY) != 1):
            continue
        if (gcd(q-1,E_KEY) != 1):  # using the shortcut from page 25 and 26 instead of using gcdb
            continue
        break
    return (p, q)

def getModAndTotient(p,q):
    return (p*q,(p-1)*(q-1))

def getMI_D(n):
    key = BitVector( intVal = E_KEY)
    mod = BitVector( intVal = n )
    d = key.multiplicative_inverse(mod)
    return int(d)

def genKeys():
    p, q = genPrimes()
    n,totient_n = getModAndTotient(p, q)
    D_KEY = getMI_D(totient_n)
    return (E_KEY, D_KEY, n, p, q)


def encrypt(E_KEY,n):
    input_file = BitVector(filename='message.txt')
    FILEOUT = open('output.txt', 'w')
    while input_file.more_to_read:
        M = input_file.read_bits_from_file(128)
        size = M.length()
        M.pad_from_left(256 - size)
        C = ModExponent(int(M),E_KEY,n)
        #C.write_to_file(FILEOUT.getHexStringFromBitVector())
        FILEOUT.write(C.get_bitvector_in_hex())
    input_file.close_file_object()
    FILEOUT.close()

def decrypt(D_KEY,n):
    input_file = BitVector(filename='output.txt')
    FILEOUT = open('decrypted.txt', 'wb')
    while input_file.more_to_read:
        C = input_file.read_bits_from_file(256*2)
        C = BitVector(hexstring= C.getTextFromBitVector())
        D = ModExponent(int(C),D_KEY,n)
        D = D[128:256]
        D.write_to_file(FILEOUT)
    input_file.close_file_object()
    FILEOUT.close()

def ModExponent(M,E_KEY,n):
    result = 1
    while E_KEY > 0:
        if E_KEY & 1:
            result = (result * M) % n
        E_KEY = E_KEY >> 1
        M = (M * M) % n
    return BitVector(intVal = result, size = 256)

if __name__ == "__main__":
    E_KEY, D_KEY, n, p, q = genKeys()
    encrypt(E_KEY,n)
    decrypt(D_KEY,n)
    #print(D_KEY)
    #print(n)
    #print(E_KEY*D_KEY%n )


