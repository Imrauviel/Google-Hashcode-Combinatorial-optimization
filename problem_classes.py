class Problem:
    def __init__(self):
        self.n_books = None  # number of books
        self.n_libraries = None  # number of libraries
        self.days = None  # days available for supplying books
        self.scores = None # list of book scores according to book id
        self.libraries = []  # list of libraries [Library_object, Library_object, ...]
        
class Book:
    def __init__(self, bookID, bookScore):
        self.id = bookID
        self.score = bookScore

    def __lt__(self, other):
        """ Method allowing to sort Books by their score """
        return self.score < other.score
    
    def __repr__(self):
        """ Method changing how object is represented""" 
        return str(self.id)
    
    def __radd__(self, other):
        """ Method allowing to sum up scores of all books in one container"""
        return self.score + other
    
class Library:
    def __init__(self, problem, idx, book_idxs, sign_up_time, books_per_day, num_of_books, books_set):
        self.id = idx # id of particular library
        self.book_ids = book_idxs  # set of book ids available in given library
        self.books = books_set  # set of books {Book_object, Book_object, ...}
        self.value = self.determine_value() # value of all books in library

        self.sign_up_time = sign_up_time # time needed to sign up library for supplying books
        self.books_per_day = books_per_day # number of books given library may supply per day
        self.lenbooks = num_of_books # number of books

    def determine_value(self):
        """ Method to measure value of all books in Library (in certain moment)"""
        return sum(self.books)


def open_file(filename):
    with open("data/" + filename) as f:
        conttent = f.read().splitlines()
    return conttent


def get_essentials(content, problem):
    """ Function packing all read data into preffered way (to Problem, Libraries, etc.)""" ########################################
    problem.n_books, problem.n_libraries, problem.days = list(map(int, content[0].split(' ')))
    problem.scores = list(map(int, content[1].split(' ')))
    
    # Creating Book objects
    all_book_list = []
    for ids, score in enumerate(problem.scores):
        book = Book(ids, score)
        all_book_list.append(book)
        
    pos = 1
    for idx in range(problem.n_libraries):
        # Repeating so many times how many libraries there are.
        pos += 1
        num_of_books, sign_up_time, books_per_day = list(map(int, content[pos].split(' ')))
        pos += 1
        book_idxs = set(map(int, content[pos].split(' ')))
        book_set = set([all_book_list[x] for x in book_idxs])
        problem.libraries.append(Library(problem, idx, book_idxs, sign_up_time, books_per_day, num_of_books, book_set))

