class User(object):
    def __init__(self, name, email): # Initates instance for User class
        self.name=name
        self.email=email
        self.books={} # Empty dictionary, will contain user's books and ratings.

    def get_email(self):
        return("{}'s email is {}.".format(self.name,self.email))
        # Will print out email of user.

    def change_email(self, address):
        self.email=address
        print("{}'s email has been updated to {}.".format(self.name,self.email))
        # Will updates user's email address.

    def __repr__(self):
        return("\nUser: {} \nEmail: {} \nTotal books read: {}\n".format(self.name,self.email,len(self.books)))
        # Will gives details about used in easy to read format.

    def __eq__(self, other_user):
        if self.name==other_user.name and self.email==other_user.email:
            return True
            #Will return True if email address for two compared users are identical.
        else:
            return False

    def read_book(self,book,rating=None):
        self.books[book]=rating
        # Will register that a reader has read a book, with a optional rating.

    def get_average_rating(self):
        self.user_ratings=[] # Create empty list for users ratings.
        for values in self.books.values():
            if values!=None: # Ignore read book if no ratings give.
                self.user_ratings.append(values) # Add rating to list.
        try: # Returns average of all ratings (the required answer)
            return(sum(self.user_ratings)/len(self.user_ratings))
        except ZeroDivisionError:
            return None # Avoids error if user has given no ratings.
        
class Book(object):
    def __init__(self,title,isbn): # Creates book
        self.title=title
        self.isbn=isbn
        self.rating=[] # Empty list that will be used to store ratings.
    
    def __repr__(self): 
        return("{},   ISBN: {}".format(self.title,self.isbn))
        #User friendly way to present object information.
    
    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn
    
    def set_isbn(self,new_isbn): # Will change ISBN and print message
        self.isbn=new_isbn
        print("{}'s ISBN has been updated to {}.".format(self.title,self.isbn))
    
    def add_rating(self,rating): 
        if type(rating)==int and 0<=rating<=4: # Checks given rating is valid
            self.rating.append(rating) # If valid, addess to list.
        else:
            print("Invalid rating") # Error message if not valid.
    
    def __eq__(self,other_book):
        if self.isbn==other_book.isbn:
            return True
        else:
            return False
        # Used to check if IABN already used
    
    def get_average_rating(self): # Gives average rating for books
        if len(self.rating)==0: # Avoids error if not ratings given.
            return ("There are no ratings!")
        else:
            return sum(self.rating)/len(self.rating) 

    def __hash__(self): # Allows class to be key in dictionary.
        return hash((self.title,self.isbn))


class Fiction(Book): # Creates sub-class of Fiction
    def __init__ (self,title,author,isbn):
        super().__init__(title,isbn)
        self.author=author
    def get_author(self):
        return self.author
    def __repr__ (self):
        return ("{} by {}".format(self.title,self.author))

class Non_Fiction(Book): # Creates sub-class of Non-Fiction
    def __init__ (self,title,subject,level,isbn):
        super().__init__(title,isbn)
        self.subject=subject
        self.level=level
    def get_subject (self):
        return self.subject
    def get_level (self):
        return self.level
    def __repr__ (self):
        return ("{}, a {} manual on {}.".format(self.title,self.level,self.subject))

class TomeRater():
    def __init__(self):
        self.users={} # Dictionary will map user's email to user object
        # Remember, user takes in (user,name,email), but has also self.books as list of books read.
        self.books={} # Dictionary will map book object to number of user who have read

    def __repr__(self):
        users_names=[user.name for user in self.users.values()]
        books_list=[book.title for book in self.books.keys()]
        return ("\nThe users are: {}.\nThe books are: {}".format(users_names,books_list))
        #Returns list of users, then books, on two lines.

    def create_book(self,title,isbn):
        new_book=Book(title,isbn)
        check_isbn=[book==new_book for book in self.books.keys()]
        if True in check_isbn: # Prints error message if ISBN already in use
            print("ISBN already in use!")
        else:
            return(new_book)

    def create_novel(self,title,author,isbn): # Adds new novel
        new_book=Fiction(title,author,isbn)
        check_isbn=[book==new_book for book in self.books.keys()]
        if True in check_isbn:
            print("ISBN already in use!")
        else:
            return(new_book)

    def create_non_fiction(self,title,subject,level,isbn): # Adds new Non Fiction
        new_book=Non_Fiction(title,subject,level,isbn)
        check_isbn=[book==new_book for book in self.books.keys()]
        if True in check_isbn:
            print("ISBN already in use!")
        else:
            return(new_book)

    def add_book_to_user(self,book,email,rating=None): # Adds book to user with optional rating.
        if email not in self.users: # Checks user exists
            print("No user with email {}!".format(email))           
        else:
            self.users[email].read_book(book,rating) # Calls read_book method from User class.
            if book in self.books:
                self.books[book]+=1 # If book already exists, adds one to read count.
            else:
                self.books[book]=1 # If book does not exist, adds with read count of one.
            if rating!=None:
                    book.add_rating(rating) # Calls add_rating method from Book class if rating given.

    def add_user(self,name,email,user_books=None): # Adds user, with optional book list.
        new_user=User(name,email) # Creates new instance of User. Still needs to be addes to list of users
        check_exists=[user==new_user for user in self.users.values()] # Checks new instance not already used.
        check_email_valid=("@" in email and (".com" in email or ".edu" in email or ".org" in email))
        # Checks is a valid email address
        if True in check_exists:
            print ("That email already exists!")
        elif check_email_valid==False:
            print("Email address invalid!")
        else: # Only is pass tests, will add new user and book objects to dictionaries.
            self.users[email]=new_user
            if user_books!=None:
                for user_book in user_books:
                    self.add_book_to_user(user_book,email)

    def print_catalogue(self):
        for books in self.books:
            print (books)

    def print_users(self):
        for email in self.users:
            print(self.users[email])

    def get_most_read_book(self): # A method to find the most read book
        most_read_books=[] # Sets empty list for answer
        times_read=0 # 0 is minimum times possible
        for book in self.books:
            if self.books[book]>times_read:
                # If new outright winner, start new list with this book only and sets times read.
                most_read_books=[book]
                times_read=self.books[book]
            elif self.books[book]==times_read:
                # If equal to current 'winner', add to 'winner list'.
                most_read_books.append(book)
        # Flow control gives printing options for single or multiple winners.
        if len(most_read_books)==1:
            return ("\nThe most read book is {}. It has been read {} times.".format(most_read_books[0],times_read))
        else:
            return ("\nThe following have been read {} times each: {}".format(times_read,most_read_books))

    def get_n_most_read_books(self,n): # Method to find n most read books
        if n>len(self.books): # If asked for more than existing number of books, orders all books.
            n=len(self.books)
        most_read_books=[] # Sets empty list for resulting books (ordered, unlike dictionary)
        most_read_counts=[] # Sets empty list for resulting count (ordered, unlike dictionary)
        n_count=1
        while n_count<=n:# While loop will stop when n books listed.
            most_read_book=None
            times_read=-1
            for book in self.books:
                if (self.books[book]>times_read) and (book.title not in most_read_books):
                    # Finds most read book not already listed
                    most_read_book=book.title
                    times_read=self.books[book]
            most_read_books.append(most_read_book) # When book found, adds book to answer list.
            most_read_counts.append(times_read) # Add count to answer list
            n_count+=1
        return(most_read_books,most_read_counts) # Return list of n books and counts

    def print_n_most_read_books(self,n):
        # A tidy way of printing the result of get_n_most_read_books
        if n>len(self.books): # Repeat fixing error if users asks to order more books than exist.
            n=len(self.books)
        book_list,count=self.get_n_most_read_books(n)
        for i in range(n): # Calls get_n_most_read_books and prints result
            print("{} has been read {} times.".format(book_list[i],count[i]))

    def highest_rated_book(self): # A method to find book with highest average rating
        highest_rated_books=[] # Sets empty list for answers - needs to be list as could be joint winner.
        highest_rating=0 # Set current highest rating
        for book in self.books: # Iterates through all books
            if type(book.get_average_rating())==float and book.get_average_rating()>highest_rating:
                # Need to allow for average rating not existing.
                highest_rated_books=[book.title] # If new highest rating, reaplaces contents of winning list.
                highest_rating=book.get_average_rating() # Replaces contents of winning rating.
            elif type(book.get_average_rating())==float and book.get_average_rating()==highest_rating:
                highest_rated_books.append(book.title)
                #If joint with current leader(s), is added to list.
        if len(highest_rated_books)==1:
            return ("\nThe highest rated book is {}. It's rating is {}.".format(highest_rated_books[0],highest_rating))
        else:
            return ("\nThe following have the highest rating of {}. {}".format(highest_rating,highest_rated_books))
            # Two separate ways of producing result dependent on single on multiple winners.

    def most_positive_user(self): # Follows same structure as highest_rated_book
        highest_rating_users=[]
        highest_rating=0 
        for user in self.users.values():
            if type(user.get_average_rating())==float and user.get_average_rating()>highest_rating:
                highest_rating_users=[user.name]
                highest_rating=user.get_average_rating()
            elif type(user.get_average_rating())==float and user.get_average_rating()==highest_rating:
                highest_rating_users.append(user.name)
        if len(highest_rating_users)==1:
            return ("\nThe highest rating user is {}, with average rating {}.".format(highest_rating_users[0],highest_rating))
        else:
            return ("\nThe following gave the joint highest average rating of {}. {}".format(highest_rating,highest_rating_users))

    def get_n_most_prolific_readers(self,n): # Follows same structure as get_n_most_read_books
        if n>len(self.users):
            n=len(self.users)
        most_prolific_users=[]
        most_read_counts=[]
        n_count=1
        while n_count<=n:
            most_prolific_user=None
            books_read=-1
            for user in self.users:
                if (len((self.users[user]).books)>books_read) and ((self.users[user]).name not in most_prolific_users):
                    most_prolific_user=(self.users[user]).name
                    books_read=len((self.users[user]).books)
            most_prolific_users.append(most_prolific_user)
            most_read_counts.append(books_read)
            n_count+=1
        return(most_prolific_users,most_read_counts)

    def print_n_most_profilic_readers(self,n): # Follows same structure as print_n_most_read_books
        # A neater way of showing output from get_n_most_prolific_users
        if n>len(self.users):
            n=len(self.users)
        user_list,count=self.get_n_most_prolific_readers(n)
        for i in range(n):
            print("{} has read {} books.".format(user_list[i],count[i]))

    def recommend_book(self):
        # Will recommend the highest rated book a user hasn't read.
        for user in self.users.values():  #Iterates through all users
            recommended_book=None 
            recommended_rating=-1 # Sets starting conditions that will be beaten if books exists
            for book in self.books: # Iterates through all books
                 if book not in user.books and book.get_average_rating()>recommended_rating:
                     recommended_book=book.title
                     recommended_rating=book.get_average_rating()
                     # Replaces 'winner' if has higher rating.
            if recommended_book==None:
                print("{} has read all available books!".format(user.name))
                # Allow for case that user has read all books.
            else:
                print("{} should read {}. It's rating is {}.".format(user.name,recommended_book,recommended_rating))


Tome_Rater = TomeRater()
#Create some books:
book1 = Tome_Rater.create_book("Society of Mind", 12345678)

novel1 = Tome_Rater.create_novel("Alice In Wonderland", "Lewis Carroll", 12345)
novel1.set_isbn(9781536831139)
nonfiction1 = Tome_Rater.create_non_fiction("Automate the Boring Stuff", "Python", "beginner", 1929452)
nonfiction2 = Tome_Rater.create_non_fiction("Computing Machinery and Intelligence", "AI", "advanced", 11111938)
novel2 = Tome_Rater.create_novel("The Diamond Age", "Neal Stephenson", 10101010)
novel3 = Tome_Rater.create_novel("There Will Come Soft Rains", "Ray Bradbury", 10001000)

#Create users:
Tome_Rater.add_user("Alan Turing", "alan@turing.com")
Tome_Rater.add_user("David Marr", "david@computation.org")

#Add a user with three books already read:
Tome_Rater.add_user("Marvin Minsky", "marvin@mit.edu", user_books=[book1, novel1, nonfiction1])

#Add books to a user one by one, with ratings:
Tome_Rater.add_book_to_user(book1, "alan@turing.com", 1)
Tome_Rater.add_book_to_user(novel1, "alan@turing.com", 3)
Tome_Rater.add_book_to_user(nonfiction1, "alan@turing.com", 3)
Tome_Rater.add_book_to_user(nonfiction2, "alan@turing.com", 4)
Tome_Rater.add_book_to_user(novel3, "alan@turing.com", 1)

Tome_Rater.add_book_to_user(novel2, "marvin@mit.edu", 2)
Tome_Rater.add_book_to_user(novel3, "marvin@mit.edu", 2)
Tome_Rater.add_book_to_user(novel3, "david@computation.org", 4)

#Tome_Rater.print_catalogue()
#Tome_Rater.print_users()


print(Tome_Rater.most_positive_user())
print(Tome_Rater.highest_rated_book())
print(Tome_Rater.get_most_read_book())
Tome_Rater.print_n_most_read_books(8)
Tome_Rater.print_n_most_profilic_readers(4)
Tome_Rater.recommend_book()
print(Tome_Rater)