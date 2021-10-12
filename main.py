# import section

from problem_classes import *
from smart_greedy import * 
from genetic_algorithm import *
import threading
from sys import exit


def start(algorithm, data, result_format):
    """ Function running given algorithm on a given data """
    print(f"\n##########SOLUTION FOR {data} BEGINNING##########\n")
    start_time = time.time()
    holder = open_file(data)

    problem = Problem()
    get_essentials(holder, problem)
    
    time_left = time.time() - start_time
    
    alg = algorithm(problem, time_left, result_format)
    alg.calculate()
    print(f"\n##########SOLUTION FOR {data} END##########\n")
    
    
# "text interface" section


text_data = ("a_example.txt",  "b_read_on.txt", "c_incunabula.txt", "d_tough_choices.txt", "e_so_many_books.txt", "f_libraries_of_the_world.txt")



which = int(input("Choose approach you want to solve the problem with (write number): 1 = Genetic Algorithm 2 = Smart Greedy\n>>> "))
if which not in [1, 2]:
    print("### Wrong algorithm specified, try again, or read the instructions ###")
    exit(0)
    
    
result_format = input("Choose returned result format: 'p' for printing,'s' for saving to file, or 'os' for scores only\n>>> ")
if result_format not in ['p', 's', 'os']:
    print("### Wrong result method specified, try again, or read the instructions ###")
    exit(0)


while True:

    text_file = input("Choose file, type 'a', 'b', 'c', 'd', 'e', or 'f' for file you want to test given algorithm against, if you want to exit type 'exit'\n>>> ")
    
    if which == 1:
        if text_file == 'exit':
            break
        elif text_file == 'a':
            start(GA, text_data[0], result_format)
        elif text_file == 'b':
            start(GA, text_data[1], result_format)
        elif text_file == 'c':
            start(GA, text_data[2], result_format)
        elif text_file == 'd':
            start(GA, text_data[3], result_format)
        elif text_file == 'e':
            start(GA, text_data[4], result_format)
        elif text_file == 'f':
            start(GA, text_data[5], result_format)
        else:
            # trying to load different data file (MUST BE PLACED IN FOLDER: "data")
            try:
                start(GA, text_file, result_format)
            except Exception:
                print("\nSpecified file cannot be found, choose different or check if your file is placed in 'data' folder")
    elif which == 2:
        if text_file == 'exit':
            break
        elif text_file == 'a':
            start(SmartGreedy, text_data[0], result_format)
        elif text_file == 'b':
            start(SmartGreedy, text_data[1], result_format)
        elif text_file == 'c':
            start(SmartGreedy, text_data[2], result_format)
        elif text_file == 'd':
            start(SmartGreedy, text_data[3], result_format)
        elif text_file == 'e':
            start(SmartGreedy, text_data[4], result_format)
        elif text_file == 'f':
            start(SmartGreedy, text_data[5], result_format)
        else:
            # trying to load different data file (MUST BE PLACED IN FOLDER: "data")
            try:
                start(SmartGreedy, text_file, result_format)
            except Exception:
                print("\nSpecified file cannot be found, choose different or check if your file is placed in 'data' folder")

        

print("Program finishing...")
print("Thank you for choosing our lines.")