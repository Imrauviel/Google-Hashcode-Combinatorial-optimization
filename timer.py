import time


def timer_(how_long, stop_flag):
   t_start = time.time()
    
   while True:
        time.sleep(1)
        print("timer running...")
        if time.time() - t_start >= how_long:
            raise Exception('Deadline passed...')
        if stop_flag:
            print("stopping timer")
            break
        
   
        
# def timer_(how_long):
#     t_start = time.time()
    
#     while True:
#         time.sleep(1)
#         print("timer running...")
#         if time.time() - t_start >= how_long:
#             # print best found solution and "kill main"
            
#             # global stop_thread_main
#             # stop_thread_main = True
            
#             # print(alist)
#             # print("finish in timer")
#             break
#         if stop_thread_timer:
#             # print("stopping timer")
#             break