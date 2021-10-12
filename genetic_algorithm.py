import random
import time

class GA:

    def __init__(self, problem, time_taken, result_format):
        self.problem = problem # problem instance
        self.libraries_idx_set = {lib.id for lib in self.problem.libraries} #set of libraries indexes 

        self.time_taken = time_taken # time taken for packing data etc.
        self.result_format = result_format # denermining how to present the results

    def calculate(self):
        timer = time.time()
        population = self.main(population_size = 50, epochs = 400, new_individuals = 20, tournamet_size = 7, prob_mutation = 0.1, time_per_run = 295 - self.time_taken)
        best_order = population[0][0]
        best_points = population[0][1]

        if self.result_format == 'os':
            print("Best Result: ", best_points, "Takes: ",time.time() - timer,"seconds")
        elif self.result_format == 'p':
            self.result_print(best_order)
        else:
            self.final_pack(best_order)
        
    def main(self, population_size,  epochs, new_individuals, tournamet_size, prob_mutation,  time_per_run):

        
        library_order = self.libraries_idx_set # set of indexes of libries in problem 
                                                             # books in i's library
        #population have form [[some libraries order, fitness of this order], [some libraries order, fitness of this order], ...]
           
        timer = time.time()
        population = self.initial_population(population_size, library_order) #create initial population
        population.sort(key = lambda x:x[1], reverse = True) #sort initial population by their fitness
                    

        #MAIN LOOP
        for epoch in range(epochs):
            if time.time()-timer > time_per_run:
                # print("Last Epoch:", epoch)
                break

            

            for k in range(new_individuals//2): #adding new individual, 2 child per 2 parents
                parents = self.TournamentSelection(population_size, tournamet_size) #select parents indexes that going to reporduce
                parents = [population[parents[0]][0] ,population[parents[1]][0]] #change indexes into actual parents
                child1, child2 = self.Crossover(parents) #create new guys
                population.append(self.fitness(child1)) #callualte theire fitnness, and add to population
                population.append(self.fitness(child2))

            population.append(population[0])#add to poulation best in previous, to save him despite mutation

            
            if self.problem.n_libraries != 2: #just to ommit a
                for m in range(population_size+new_individuals): #mutate population, and callulate new fitness of mutated individuals 
                    if random.random() <= prob_mutation: #mutate only in some prob_mutation rate
                        
                        population[m][0] = self.mutation_easy(population[m][0]) #replace individual  with his mutated version 
                        
                        population[m] = self.fitness(population[m][0]) #calulate new fitness
                        
            population.sort(key = lambda x:x[1], reverse = True) #sort population
            
            population = population[:population_size]#cut to poppulation size
            
        
        return population
        

    def initial_population(self, population_size, set_of_idx):
        ''' return list in form [[random_order_of_libries, fitness], [random_order_of_libries, fitness], 
        [random_order_of_libries, fitness] ......] '''
        population = []
        for i in range(population_size):
            indvidual = None
            indvidual = list(set_of_idx)
            random.shuffle(indvidual)
            population.append(self.fitness(indvidual))

        return population
    
    def fitness(self, library_order):
        ''' calculate fitness in this manner:
            0. day = 0,  choosen_books = None 
            1. Take first library in library_order(current_library), add to day "current_library.sign_up_time"
            2. Take all books that are not already taken
            3. Sort them according to their score
            4. Take n first, where n is lesser from [len(avlaible_books), current_library.books_per_day*(problem.days-day)]
            5. Add them to choosen_books
            6. Repeat 2-6 for each library in library_order, until day <= problem.days; no more time for more libraries, so cut rest from individual
            7. Calulate sum of taken books
        '''
        day = 0
        result = 0
        choosen_books = set()
        
        for idx in range(len(library_order)):
            lib_idx = library_order[idx]
            sums = 0 
            current_library = self.problem.libraries[lib_idx]
            day += current_library.sign_up_time

            if day < self.problem.days:
                temp = list(self.problem.libraries[lib_idx].book_ids - choosen_books)
                temp = self.sorting(temp)

                flag = min((self.problem.days - day)*current_library.books_per_day, len(temp))
                choosen_books.update(temp[:flag])
                sums += flag
            else:
                library_order = library_order[:idx]
                break
        for book in choosen_books:
            result += self.problem.scores[book]        
        return [library_order, result] 

    def TournamentSelection(self, population_size, tournamet_size):
        '''
        return: indexes of parents in population
        '''
        metting_pool = []
        number_of_parents = 2
        indexes = set(i for i in range(population_size))
        for p in range(number_of_parents):
            tournamet = set()
            for k in range(tournamet_size):
                tournamet.add(random.choice(tuple(indexes-tournamet)))
            tournamet = min(tournamet) # we know that population is sorted, therefor minimal index have maximal value  
            indexes = indexes - set([tournamet])# avoid reproducing with itself
            metting_pool.append(tournamet)
        return metting_pool

    def Crossover(self, parents):
        '''
            For both children, save the genes that are common in both parents where they were in the respective parents
            Then, for child1 in empty genes put first non taken from parent2, and then put the rest randomly among not choosen already. Reapeat for                 child2 respectively
        '''
        
        length = max(len(parents[0]), len(parents[1]))

        parent1_set = set(parents[0])
        parent2_set = set(parents[1])
        common_set = parent1_set & parent2_set

        not_in_child1, not_in_child2 = [], []
        child1, child2 = [None]*length, [None]*length

        for i in range(len(parents[0])):
            if parents[0][i] in common_set:
                child1[i] = parents[0][i]
            else:
                not_in_child1.append(parents[0][i])

        for i in range(len(parents[1])):
            if parents[1][i] in common_set:
                child2[i] = parents[1][i]
            else:
                not_in_child2.append(parents[1][i])

        for i in range(length):
            if child1[i] == None:
                if len(not_in_child2) > 0:
                    child1[i] = not_in_child2.pop(0)
                else:
                    child1[i] = random.choice(tuple(self.libraries_idx_set - parent2_set - set(child1)))
            if child2[i] == None:
                if len(not_in_child1) > 0:
                    child2[i] = not_in_child1.pop(0)
                else:

                    child2[i] = random.choice(tuple(self.libraries_idx_set - parent1_set - set(child2)))
        
        return child1, child2
        


    def mutation_easy(self, individual):
        '''
        Choose one, not already choosen library, and add it to begging of individual, then sometimes shuffle all 
        '''
        possible_values = self.libraries_idx_set - set(individual)

        if len(possible_values) > 0:
            new_value = random.choice(tuple(possible_values))
            
            individual = [new_value] + individual
            if random.random()<0.2:
                random.shuffle(individual)
        else:
            random.shuffle(individual)
            
        return individual


    def sorting(self, books): 
        ''' 
        Sort books according to their score
        '''
        temp_name = { i: self.problem.scores[i] for i in books}
        temp_name = sorted(temp_name.items(), key = 
             lambda kv:(kv[1], kv[0]), reverse=True)
        books = [key[0] for key in temp_name]
        return books

    def final_pack(self, libraries_order):
        """ 
        Method writing out the results in a Google HashCode format to the file called results.txt .
        It might be useful to check the solution as stdout sometimes is not able to fit all text.
        """
        day = 0
        book_for_scaning = []
        choosen_books = set()
       
        for lib_id in libraries_order:
            current_libries = self.problem.libraries[lib_id]
            day += current_libries.sign_up_time
            if day <= self.problem.days:
                temp = list(current_libries.book_ids - choosen_books)
                temp = self.sorting(temp)
                flag = min((self.problem.days - day) * current_libries.books_per_day, len(temp))
                book_for_scaning.append(temp[:flag])
                choosen_books.update(temp[:flag])


        file = open("result.txt", "w+") 
        file.write(str(len(book_for_scaning)))  
        file.write("\n")    
        for k in range(len(book_for_scaning)):

            file.write(str(libraries_order[k]))
            file.write(" ")
            file.write(str(len(book_for_scaning[k])))
            file.write("\n") 
            
            file.write(" ".join(str(x) for x in book_for_scaning[k]))  
            file.write("\n") 
        file.close()
        

    def result_print(self, libraries_order):
        """ Method printing out the results in a way indicated by Google HashCode rules to stdout"""
        day = 0
        book_for_scaning = []
        choosen_books = set()
       
        for lib_id in libraries_order:
            current_libries = self.problem.libraries[lib_id]
            day += current_libries.sign_up_time
            if day <= self.problem.days:
                temp = list(current_libries.book_ids - choosen_books)
                temp = self.sorting(temp)
                flag = min((self.problem.days - day) * current_libries.books_per_day, len(temp))
                book_for_scaning.append(temp[:flag])
                choosen_books.update(temp[:flag])


        print(len(book_for_scaning))
        for k in range(len(book_for_scaning)):
            
            print(libraries_order[k], len(book_for_scaning[k]))
            print(" ".join(str(x) for x in book_for_scaning[k]))
            
