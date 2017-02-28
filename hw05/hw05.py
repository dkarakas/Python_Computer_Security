#! /bin/python

#Homework Number:hw05
#Name:Dimcho karakashev
#ECN Login: dkarakas
#Due Date: 02/10/17

import BitVector
from copy import deepcopy

class RC4:


    def __init__(self,key):
        self.key = self.generate_S_Vector(key);

    def generate_S_Vector(self,key):
        S = []
        T = []
        for i in range(0,256):
            S.append(i)
            T.append(key[i % len(key) ])

        j = 0
        for i in range(0,256):
            j = (j + S[i] +ord(T[i])) % 256
            S[i], S[j] = S[j], S[i]
        return S

    def encrypt(self,dataToEncrypt):
        i = 0
        j = 0
        encrypted_output = ""
        copy_key = deepcopy(self.key)
        for data in dataToEncrypt:
            i = (i + 1) % 256
            j = (j + copy_key[i]) % 256
            copy_key[i], copy_key[j] = copy_key[j], copy_key[i]
            k = ( copy_key[i] + copy_key[j]) % 256
            encrypted_output += chr(copy_key[k] ^ ord(data))#making the assumption that we are passing string(data is a char)
        return encrypted_output

    def decrypt(self,dataToEncrypt):
        i = 0
        j = 0
        encrypted_output = ""
        copy_key = deepcopy(self.key)
        for data in dataToEncrypt:
            i = (i + 1) % 256
            j = (j + copy_key[i]) % 256
            copy_key[i], copy_key[j] = copy_key[j], copy_key[i]
            k = ( copy_key[i] + copy_key[j]) % 256
            encrypted_output += chr(copy_key[k] ^ ord(data)) #making the assumption that we are passing string(data is a char)
        return encrypted_output

def openFile(fileName):
    header = []
    data = []
    with open(fileName,"rb") as fileInput:
        for i in range(0,3):
            header.append(fileInput.readline())
        data = fileInput.read()
    return (header, data)

if __name__ == "__main__":
    init = RC4("Cool key")
    header, data = openFile("winterTown.ppm")

    head_str = ""
    read_str = ""

    for i in range(0,3):#converting the bytes into a string
        for j in range(0, len(header[i])):  # converting the bytes into a string
            head_str += chr(header[i][j])
    print(header)
    print(head_str)
    for i in range(0,len(data)):#converting the bytes into a string
        read_str += chr(data[i])

    encrypted = init.encrypt(read_str)
    decrypted = init.decrypt(encrypted)

    if read_str == decrypted:
        print("Good to go")
    else:
        print("some issue")


    with open("output.ppm","w+") as encryptedPic:
        encryptedPic.write(head_str)
        encryptedPic.write(decrypted)

