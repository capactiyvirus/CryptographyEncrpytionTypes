#!/usr/bin/env python
#imports
import sched
import time
import os




event_schedule = sched.scheduler(time.time, time.sleep)

def do_something():
    print("Hello, World!")
    print(os.getpid())
    event_schedule.enter(5, 1, do_something)

#event_schedule.enter(5,1,do_something)
#event_schedule.run()

def xor():
    print("Hello, World!")


def aes():
    print("Hello, World!")




def rc4():
    print("Hello, World!")


def blowfish():
    print("Hello, World!")



def run( folder, types, secrets, action):
    print("Hello, World!")
    print(folder + types + secrets+ action)



def main():
    run("hello","pope","yum","lips")




if __name__ == "__main__":
    main()



#implemintation 
#we need to take a 