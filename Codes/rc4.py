#!/usr/bin/env python3

from pathlib import Path
import numpy
import struct
import os
import re
import binascii
import base64
from itertools import cycle
import magic

S = list()


Key = "Key"






#we need our key to be at least 256 bits


for root, dirs, files in os.walk("testDir"):
        for file1 in files:
        
            # data can be held in differnt formats which mean we have to account for them.
            data = open(os.path.join(root,file1),"rb+")

            dataValue = data.read()
            print(dataValue)
            j = 0
            for i in range(256):
                if j <= len(Key)-1:
                    S.append(bytearray(Key[j].encode("latin_1")))
                    j+=1
                    
                    
                else: 
                    j = 0
                    S.append(bytearray(Key[j].encode("latin_1")))
                    j+=1
                #print(j)
                #print(str(list(S[i])))
                

           # value = bytes(list((x^ord(y)) for (x,y) in zip(dataValue,cycle(xorKey))))



for i in range(len(S[3])):
    print(S[3][i])


print(len(S))