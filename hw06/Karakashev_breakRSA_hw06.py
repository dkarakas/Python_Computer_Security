#!/usr/bin/env python

from PrimeGenerator import PrimeGenerator
from BitVector import *
import numpy as np
import sys

#Homework Number: hw06
#Name: Dimcho Karakashev
#ECN Login: dkarakas
#Due Date: 02/23/17


#As specified by the assignment
E_KEY = 3

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


def encrypt(E_KEY,n,filename):
    input_file = BitVector(filename='message.txt')
    FILEOUT = open(filename, 'w')
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

def break_RSA(filename_1,filename_2,filename_3,n_1,n_2,n_3):
    input_file_1 = BitVector(filename=filename_1)
    input_file_2 = BitVector(filename=filename_2)
    input_file_3 = BitVector(filename=filename_3)
    n_tot = n_1*n_2*n_3
    while input_file_1.more_to_read:
        C_1 = input_file_1.read_bits_from_file(256 * 2)
        C_2 = input_file_2.read_bits_from_file(256 * 2)
        C_3 = input_file_3.read_bits_from_file(256 * 2)
        C_1 = BitVector(hexstring=C_1.getTextFromBitVector())
        C_2 = BitVector(hexstring=C_2.getTextFromBitVector())
        C_3 = BitVector(hexstring=C_3.getTextFromBitVector())
        M_1 = n_2 * n_3
        M_2 = n_1 * n_3
        M_3 = n_1 * n_2
        M_1_inv = (BitVector(intVal=M_1)).multiplicative_inverse(BitVector(intVal=n_1))
        M_2_inv = (BitVector(intVal=M_2)).multiplicative_inverse(BitVector(intVal=n_2))
        M_3_inv = (BitVector(intVal=M_3)).multiplicative_inverse(BitVector(intVal=n_3))
        C_1_vals = (int(C_1) % n_1,int(C_1) % n_2,int(C_1) % n_3)
        C_2_vals = (int(C_2) % n_1, int(C_2) % n_2, int(C_2) % n_3)
        C_3_vals = (int(C_3) % n_1, int(C_3) % n_2, int(C_3) % n_3)
        result_vals = (C_1_vals[0] * C_2_vals[0] * C_3_vals[0] % n_1, \
                       C_1_vals[1] * C_2_vals[1] * C_3_vals[1] % n_2, \
                       C_1_vals[2] * C_2_vals[2] * C_3_vals[2] % n_3)
        m_cubed = (result_vals[0] * M_1 * int(M_1_inv) + result_vals[1] * M_2 * int(M_2_inv) + result_vals[2] * M_3 * int(M_3_inv)) % n_tot
        print(m_cubed)
        plain_message = solve_pRoot(3, m_cubed)
        print(plain_message)
    input_file_1.close_file_object()

def solve_pRoot(p,y):
    """GIVEN FUNCTION"""
    p = np.long(p);
    y = np.long(y);
    # Initial guess for xk
    try:
        xk = np.long(pow(y,1.0/p));
    except:
        # Necessary for larger value of y
        # Approximate y as 2^a * y0
        y0 = y;
        a = 0;
        while (y0 > sys.float_info.max):
            y0 = y0 >> 1;
            a += 1;
        # log xk = log2 y / p
        # log xk = (a + log2 y0) / p
        xk = np.long(pow(2.0, ( a + np.log2(float(y0)) )/ p ));

    # Solve for x using Newton's Method
    err_k = np.long(pow(xk,p))-y;
    while (abs(err_k) > 1):
        gk = p*np.long(pow(xk,p-1));
        err_k = np.long(pow(xk,p))-y;
        xk = np.long(-err_k/gk) + xk;
    return xk



if __name__ == "__main__":
    E_KEY_1, D_KEY_1, n_1, p_1, q_1 = genKeys()
    E_KEY_2, D_KEY_2, n_2, p_2, q_2 = genKeys()
    E_KEY_3, D_KEY_3, n_3, p_3, q_3 = genKeys()
    encrypt(E_KEY_1, n_1, "Encrypt_E_3_1.txt")
    encrypt(E_KEY_2, n_2, "Encrypt_E_3_2.txt")
    encrypt(E_KEY_3, n_3, "Encrypt_E_3_3.txt")
    break_RSA("Encrypt_E_3_1.txt", "Encrypt_E_3_2.txt", "Encrypt_E_3_3.txt", n_1, n_2, n_3)
