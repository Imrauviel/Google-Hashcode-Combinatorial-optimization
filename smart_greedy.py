from math import ceil
import time
import threading

class SmartGreedy:
    def __init__(self, problem, time_taken, result_format):
        self.problem = problem # problem instance
        self.libraries_scanned = 0  # number of scanned libraries
        self.libraries_order = {}  # keys = libraries_sign_up_order, values: [library.id, set_of_book_ids_supplied_by_given_library]
        self.already_supplied_books = set() # set of all supplied books
        self.new_already_supplied_books = set() # set of new supplied books 
        self.total_points = 0 # total points got from all supplied books
        
        self.time_taken = time_taken # time taken for packing data etc.
        self.stop_timer = False # stopping timer flag
        
        self.stop_calculate = False # stopping calculate flag
        
        self.result_format = result_format # denermining how to present the results
        
        
    def timer_(self, whole_time):
        """
            Method making sure that algorithm finishes in given time
            It either finishes, or returns what it was able to count until time passed
        """
        time_start = time.time()
        time_left_ = whole_time - self.time_taken
        while True:
             time.sleep(0.25) # to save resources state is checked every 0.25 second (it does not create a big mistake when overtiming)
             if time.time() - time_start >= time_left_:
                 # Greedy did not managed to finish in specified time
                 # It should not happen, for all given data (from a to f) the longest time needed for algoritm was 1 minute 29 seconds for d example
                 # Stop looking for better solution and print the one found till now!
                 print("Greedy did not managed to finish in specified time")
                 self.stop_calculate = True
                 break
             
             elif self.stop_timer == True:
                # Greedy managed to finish earlier
                # kill the thread (simply finish it's code)
                run_time = time.time() - time_start
                print(f"Program managed to finish earlier in {round(run_time + self.time_taken, 2)} seconds")
                break
            
        
    def remove_new_already_supplied(self, library):
        """ Method removing newly supplied books from given library """
        library.books.difference_update(self.new_already_supplied_books)        
        
        
    def update_libraries(self, days_left, libraries_to_update):
        """ 
            Method updating estimated values assigned to not signed yet libraries 
            and ordering libraries in prefered way to sign up (the highest estimated score first)
        """
        return_libs = []
        for lib in libraries_to_update:
            available_time = days_left - lib[1].sign_up_time
            if available_time <= 0:
                continue
                # No time left to sign up given library, thus algorithm simply does not take it into consideration later on.
            else:
                # There is enough time left to sign particular library
                self.remove_new_already_supplied(lib[1]) # Removing duplicated books from library
                library_value = self.determining_value(lib[1], days_left) # Determining estimated value of given library
                if library_value == 0:
                    continue
                    # There are no unique books in given library (or given books has no value) -> get next library
                else:
                    # There are unique books in library
                    return_libs.append([library_value, lib[1]])

        return_libs.sort(key=lambda x: x[0], reverse = True)  # sort libraries in descending order by estimated score they can provide
        self.new_already_supplied_books = set() # Reseting newly supplied books to empty set
        return return_libs

    
    def determining_value(self, library, days_left):
        """
            Method determining the value of books possible to supply in indicated time from certain library
            multiplied by 1 over sign up time of the library, thus this approximation take into account
            not only books scores but also sign up time giving the best (so far) results.  
        """
        available_days = days_left - library.sign_up_time
        books_number = min(len(library.books), available_days*library.books_per_day)
        
        ordered_books = list(library.books) # changing set to list (sorting possible)
        ordered_books.sort(reverse = True) # ordering books with respect to their score in descending order
        ordered_books = ordered_books[0:books_number] # determining possible to supply books
        return sum(ordered_books) * (1/library.sign_up_time)
        

    def supply_books(self, library, number_of_books_to_deliver):
        """ Method that add books from given library to already supplied books"""
        self.libraries_order[self.libraries_scanned-1] = [library.id, set()] # saving sign up order of libraries and books they supplied (INITIALIZATION)
        book_number = min(len(library.books), number_of_books_to_deliver) # determining max possible number of books to supply
        ordered_books = list(library.books)
        ordered_books.sort(reverse = True) 
        ordered_books = ordered_books[0:book_number] # cutting books that will not be able to be supplied
        
        ordered_books = set(ordered_books)
        
        self.already_supplied_books.update(ordered_books) # adding new books to all already supplied
        self.new_already_supplied_books.update(ordered_books) # adding those books here to determine later what books to delete in all other libreries (have already been supplied)
        self.libraries_order[self.libraries_scanned-1][1].update(ordered_books) # saving sign up order of libraries and books they supplied


    def calculate(self):
        """ Main function of the class, solves the problem by SmartGreedy approach"""

        timer_thread = threading.Thread(target=self.timer_, args=[300])
        timer_thread.start()
        
        days_left = self.problem.days # days left to finish signing up libraries
        update_count = ceil(days_left / 1000) # seting template of how often order of libraries will be updated, HERE set to approximately 1000 times
        update_count_ = 1 # setting to 1 to update libraries in first iteration
        libraries_off = [[1, lib] for lib in self.problem.libraries]  # initializing list of libraries waiting to sign up (just to match required format)
        
        # print("Number of all libraries in given problem:", self.problem.n_libraries, ",days left:", days_left, ",update count:", update_count)
        
        while days_left > 0:
            # print("DAYS LEFT:", days_left) 
            update_count_ -= 1
            if update_count_ == 0:
                # Updating ordering of libraries to be signed up
                libraries_off = self.update_libraries(days_left, libraries_off)
                update_count_ = update_count
            if len(libraries_off) > 0:
                # There is at least 1 library to choose so:
                # Selecting most promising library to sign it up
                selected_library = libraries_off.pop(0)[1]
                self.libraries_scanned += 1
                # Substracting time needed to sign it up from available
                days_left -= selected_library.sign_up_time
                # Determining number of books that selected library may supply
                num_of_books_to_deliver = days_left * selected_library.books_per_day
                # Suppling umber of books from given library
                self.supply_books(selected_library, num_of_books_to_deliver)
            else:
                break
                # No available libraries to sign up -> end
            if self.stop_calculate:
                break
            
        self.stop_timer = True
        timer_thread.join()
        
        if self.result_format == 'p':
            self.result_print() # Printing result in Google Hashcode format 
        elif self.result_format == 's':
            self.result_save() # Saving results in Google Hashcode format to results.txt
        elif self.result_format == 'os':
            self.sum_up_points() # Giving only the score of all supplied books
                

    def result_print(self):
        """ Method printing out the results in a way indicated by Google HashCode rules to stdout"""
        print(self.libraries_scanned)
        for libnum in range(self.libraries_scanned):
            print(self.libraries_order[libnum][0], len(self.libraries_order[libnum][1]))
            for book_id in self.libraries_order[libnum][1]:
                print(book_id, end=" ")
            print("\n")


    def result_save(self):
        """ 
        Method writing out the results in a Google HashCode format to the file called results.txt .
        It might be useful to check the solution as stdout sometimes is not able to fit all text.
        """
        with open("results.txt", 'w') as f:
            f.write(str(self.libraries_scanned)+'\n')
            
            for libnum in range(self.libraries_scanned):
                f.write(f"{self.libraries_order[libnum][0]} {len(self.libraries_order[libnum][1])}\n")
                for book_id in self.libraries_order[libnum][1]:
                    f.write(f"{book_id} ")
                f.write("\n")
            
            
    def sum_up_points(self):
        """ Method determining and printing only sum of points from all supplied books"""
        self.total_points = sum(self.already_supplied_books)
        print("All supplied books give score of:", self.total_points, "points.")