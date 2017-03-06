#!/usr/bin/env python

from PrimeGenerator import PrimeGenerator
from BitVector import *
import numpy as np
import sys

#Homework Number: hw06
#Name: Dimcho Karakashev
#ECN Login: dkarakas
#Due Date: 02/23/17



#Encrypted e_1
#n_1
# 86343468598341748745769041635620243711670550317347235461015411782
# 722342068097
#Encrypted 1
#b361eb1318de696a030845da43a44489cf86eb58f422cb
# 0eaebc4d9128483e9a7ae984ff3b83c642bd7a58498d3
# 736de26d681449c1949af25d8eb3bf629efc3a13fd59a
# f7736eb5cb361e1f739c0d2b76463af40cb2cb743a6bd
# abfca7cde40b63555efd275c401c53da109d7f53f8907
# de43d5f2fa24e985da335cdd7b82fa8cbedc62520fa7d
# 3e85ecdba2e0190b7ff492fa3f237df9b6bedc444f658
# 721fa35eb170e58c39c88e4251a63489efdaf6e1cad70
# b9c0c54fb8f7845b04583c30626273a42c1071e68ec76
# 0ec7b68100d0c36affed8d5b65effeea60c114ff65829
# f95b3e9451f5d83b2f351cff700bb566fc08344f5e2b4
# b2b0248e110da7b22f847e2bca9fac98156329c98a19f
# bdc1d2c5a6ec04d30f6994afa50b56dd71612a9e42bcd
# 091cb33805cdd0b7514931e2472bf99fb5e09d15dd953
# f013c068b9c4fecce1c9edea5f35bfba2779c53861072
# 15b1ac306258aed29f19127bcf4c398885183a0235020
# 9e7ce14c1415c6cf0ce3c12e1bae00464a907a82cfbe755

#n_2
#  1042061685035954449583944417122960207209185774459589471501761147
# 77431459874943
#e243ddb70b6407a0341b94623ef863545e59ecb518ec49
# 1e79407fa3c9532bbae64f17de1570c8f520b51e0aa04
# dfeb980bea9a0691c05db22ff532fbf7cfd7906828261
# 7ad45e78aaad900be8efde5c41c16ef85564dc4676c90
# 038512c1922175d2e0b44e4ab22c8281110d0d4b7325a
# dd6b7d7775ca885621f56ae627f33be4f62d2233d593b
# 29d9daf3aba06fbfe1d02a969469dd3ab4620903d60d7
# ba480209a97342496a0b6fb3037a7c40bd59e37fd154b
# a4d309f21453ccddd58cebbc8904a41b2940f07382f22
# 6f79fa2bc58c7e81617c99e7ec51d5d9d70dda9d83c26
# 7b8d2902bc149093b9f64bc0ba90b6dc3e8cf691a7c31
# 14b4f7025e5419c19da93f8385af24c8fdeff794ccb4d
# 737f445ddd9d420f90cdfa8fd7cd84843f32fed5ab16c
# 4d8456ff7493e35f8092f7ed95d704954d5d1883da81a
# 6e9a3703242efb992a18886a18e6837104d4143df91dd
# 902144c416b364cb2370746c588875048800ed19e6776
# 0e3f22853c7dabe887f6987d14fe8c5774d0be3b944be38

#n_3
# 11391251451021909172992013020190606497731358711768752155608307978
# 3589955855139
#72c910a34a282ca6d5b202d3607b4c4843269e5cc9e006
# 65100f9f8a09cf6180f6e66581a39ec7f1b16cad52f0d
# 76aafc6408cceaad7d20c96179318bb4a1d8ec3036108
# fb803238b6a5d4defb304f6b005771916f4813cf7adf6
# 413c13e156c92c7c72a5dfa0ee0af3a9ab1016d7d40b0
# 84c3a731a4380b4c42076724ad82110c4ad3214407e06
# 99ae619aaf92e0171835fefd222c33f2500da1ce45519
# 0513f769cfffa3d485c98e674e181fd6c92c5ad16b664
# 86ce7efabaf6389af5f884f0e2a00ba26b33b17780841
# 33c05d81e7d0c6942dbb3ca06986acaf75bf6da970a94
# 42aa7c7ac300b020712a380e1b343cc86de03832cdcd9
# ccd31fbd006c51f1a69e286be881da71fe8a578a8775f
# e9a5cb340cfaa90d6e96ae6aec0a4a2d941b287fdc2e9
# 11c05780884eb8445351458131a7f0debb504d5a1bda1
# 0e391e56d0411be3411a7a0c177bbe27cc62bd5c641ef
# 88ad358375a6c7f1b6656bfd20cba2b255a88dd30a700
# 8cdc1da36fee6010259a3d64bfb54c7feed35c93b08905e


# The breaking outputs only 0s for some reason

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
        m_cubed = int((result_vals[0] * M_1 * int(M_1_inv) + result_vals[1] * M_2 * int(M_2_inv) + result_vals[2] * M_3 * int(M_3_inv)) % n_tot)
        plain_message = solve_pRoot( m_cubed, float(1.0/3.0))
        print(plain_message)
    input_file_1.close_file_object()

def solve_pRoot(p,y):
    """GIVEN FUNCTION"""
    p = long(p);
    y = long(y);

    # Initial guess for xk
    try:
        xk = long(pow(y,1.0/p));
    except:
        # Necessary for larger value of y
        # Approximate y as 2^a * y0
        y0 = y;
        a = 0;
        while (y0 > sys.float_info.max):
            y0 = y0 >> 1;
            a += 1;
        xk = long(pow(2.0, ( a + np.log2(float(y0)) )/ p ));

    # Solve for x using Newton's Method
    err_k = long(pow(xk,p))-y;
    while (abs(err_k) > 1):
        gk = p*long(pow(xk,p-1));
        err_k = long(pow(xk,p))-y;
        xk = long(-err_k/gk) + xk;
    return xk




if __name__ == "__main__":
    E_KEY_1, D_KEY_1, n_1, p_1, q_1 = genKeys()
    E_KEY_2, D_KEY_2, n_2, p_2, q_2 = genKeys()
    E_KEY_3, D_KEY_3, n_3, p_3, q_3 = genKeys()
    encrypt(E_KEY_1, n_1, "Encrypt_E_3_1.txt")
    encrypt(E_KEY_2, n_2, "Encrypt_E_3_2.txt")
    encrypt(E_KEY_3, n_3, "Encrypt_E_3_3.txt")
    print(n_1,n_2,n_3)
    break_RSA("Encrypt_E_3_1.txt", "Encrypt_E_3_2.txt", "Encrypt_E_3_3.txt", n_1, n_2, n_3)
