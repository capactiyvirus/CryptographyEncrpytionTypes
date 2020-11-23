from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt
from pathlib import Path
import numpy
import struct
import os
import re
import binascii
import base64
from itertools import cycle


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
    for root, dirs, files in os.walk("testDir"):
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
    for root, dirs, files in os.walk("testDir"):
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
           

            print(skVal)
            decryptdata = decrypt(skVal,dataValue)
            
            #rewrite to file
            data.write(decryptdata)
            data.truncate()
            data.close()


#main Part
encrpytECC()
decryptECC()
