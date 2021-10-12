# threads: sharing 

import time
import threading

def one(bnum):
    

    while True:
       time.sleep(1)
       print("main running!")
       bnum += 1
       if bnum > 10:
           # kill thread, print solution
           global stop_thread_timer # killing thread
           stop_thread_timer = True
           print(alist) # solutions
           print("finish in main")
           break
       if stop_thread_main:
           print("stopping main")
           break
       alist.append(bnum)

def timer_(given_time):
    t_start = time.time()
    while True:
        time.sleep(1)
        print("timer running...")
        if time.time() - t_start >= given_time:
            # print best found solution and "kill main"
            global stop_thread_main
            stop_thread_main = True
            
            print(alist)
            print("finish in timer")
            break
        if stop_thread_timer:
            print("stopping timer")
            break
    
    
    

global stop_thread_timer
global stop_thread_main

stop_thread_timer = False
stop_thread_main = False

global alist
alist = []


t1 = threading.Thread(target=one, args=[5])  
t2 = threading.Thread(target=timer_ , args=[10])
t1.start()
t2.start()
t1.join()
print("lool")
t2.join()
print("your mom")





    
