import sqlite3
from BookGUI import *
from SynopsisGUI import *

window = Tk()
window.geometry("335x630")
window.title("Welcome")


#Database
con = sqlite3.connect("book.db")
cur = con.cursor()

try:
    cur.execute("""CREATE TABLE book (
                    `isbn` varchar(13) NOT NULL,
                    `title` varchar(256) NOT NULL,
                    `synopsis` text NOT NULL,
                    `author` varchar(60) NOT NULL,
                    `publicationYear` year(4) NOT NULL,
                    `category` varchar(20) NOT NULL,
                    `rating` float NOT NULL,
                    `count` int);
                    """)
    data = [
        ('9781250128546', 'Love Warrior', 'Love Warrior delves into the life of Glennon Doyle, a woman who battled with self-destructive behaviors, eating disorders, depression, and many more challenges before finally embracing the life she deserved and started living meaningfully while being true to herself.', 'Glennon Doyle Melton', 2016, 'Non-Fiction', 4.08, 90),
        ('9781119551416', 'Testing Business Ideas', 'Testing Business Ideas highlights the importance of trial and error, learning from mistakes and prototypes, and always improving your offerings in a business, so as to bring a successful product to the market that will sell instead of causing you troubles.', 'David J. Bland', 2019, 'Non-Fiction', 4.33, 50),
        ('9780393609394', 'Astrophysics for People in a Hurry', 'Astrophysics for People in a Hurry talks about the laws of nature, physics, astronomy, and the mysterious inception of our cosmos, the universe, stars, and implicitly our beautiful planet where life thrives and perpetuates.', 'Neil deGrasse Tyson', 2017, 'Non-Fiction', 4.09, 100),
        ('9781451686579', 'Contagious: Why Things Catch On', 'Contagious illustrates why certain ideas and products spread better than others by sharing compelling stories from the world of business, social campaigns, and media.', 'Jonah Berger', 2013, 'Non-Fiction', 3.97, 40),
        ('9780593328972', 'The Practice: Shipping Creative Work', 'The Practice talks about ways to enhance your creativity, boost your innovation, upgrade your creative process, and most importantly, get disciplined in your practice and turn your hobby into a professional endeavor.', 'Seth Godin', 2020, 'Non-Fiction', 4.03, 30),
        ('9780525564201', 'My Sister, the Serial Killer', 'A short, darkly funny, hand grenade of a novel about a Nigerian woman whose younger sister has a very inconvenient habit of killing her boyfriends.', 'Oyinkan Braithwaite', 2019, 'Fiction', 3.7, 90),
        ('9780593086865', 'Blue Flowers', 'Blue Flowers alternates between letters detailing the dissolution of a relationship, and is a dark portrait of desire, undermining accepted truths about love and sex, violence and fear, men and women.', 'Carola Saavedra', 2021, 'Fiction', 2.9, 40),
        ('9780143133605', 'The New Me', 'Darkly hilarious and devastating, The New Me is a dizzying descent into the mind of a young woman trapped in the funhouse of American consumer culture.', 'Halle Butler', 2019, 'Fiction', 3.4, 50),
        ('9780593197066', 'Dying in a Winter Wonderland', 'In the town of Rudolph, New York, the Christmas season should make spirits bright, but as the year comes to an end, so does life, in the fifth installment of this charming cozy mystery series.', 'Vicki Delany', 2020, 'Fiction', 4.1, 60),
        ('9780593334324', 'The Stand-Up Groomsman', 'A bridesmaid and groomsman put their differences aside to get their friends down the aisle in this opposites-attract steamy romantic comedy.', 'Jackie Lau', 2022, 'Fiction', 3.8, 39),]

    cur.executemany("INSERT INTO book VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)

    con.commit()
except:
    print("Book table already exists")


def displayChange():
    global current
    display(current)

#display one book
def display(index):
    print('here')
    global current
    global product
    cur.execute("select * from book")
    currentBook = cur.fetchall()[index]
    current = index
    entry2.delete(0, END)
    entry2.insert(END, currentBook[0])
    entry3.delete(0, END)
    entry3.insert(END, currentBook[1])
    entry4.delete(0, END)
    entry4.insert(END, currentBook[2])
    entry5.delete(0, END)
    entry5.insert(END, currentBook[3])
    entry6.delete(0, END)
    entry6.insert(END, currentBook[4])
    bookCat = currentBook[5]
    categoryTypeVar.set(bookCat)
    entry9.delete(0, END)
    entry9.insert(END, currentBook[6])
    entry8.delete(0, END)
    entry8.insert(END, currentBook[7])

#display all books in other window
def displayAll():
    cur.execute("select * from book")
    books = cur.fetchall()
    displayDialog(window, books)

#display the synopsis of a book
def displaySynopsis():
    cur.execute("select synopsis from book where isbn = \'" + entry2.get() + "\'")
    book = cur.fetchall()
    displayDialog3(window, book)

#display books based on the title searched
def cmdTitleDisplay():
    title = entry10.get()
    cur.execute("select * from book where upper(title) like ?", ('%'+title+'%',))
    books = cur.fetchall()
    displayDialog(window, books)

#display books based on author searched
def cmdAuthorDisplay():
    author = entry11.get()
    cur.execute("select * from book where upper(author) like ? ", ('%'+author+'%',))
    books = cur.fetchall()
    displayDialog(window, books)

#display book by the publication year
def cmdYearDisplay():
    year = yearTypeVar.get()
    cur.execute("select * from book where publicationYear = " + year)
    books = cur.fetchall()
    displayDialog(window, books)

#display books based on category(fiction/non-fiction)
def cmdCategoryDisplay():
    category = catTypeVar.get()
    cur.execute("select * from book where category = \'" + category + "\'")
    books = cur.fetchall()
    displayDialog(window, books)

#display books that are more than the rating chosen
def cmdRatingDisplay():
    rating = ratingTypeVar.get()
    cur.execute("select * from book where rating > " + rating);
    books = cur.fetchall()
    displayDialog(window, books)

#delete the current book
def deleteCurrentCmd():
    try:
        isbn = entry2.get()
        title = entry3.get()
        cur.execute("Delete from book where isbn = \'" + isbn + "\'")
        con.commit()
        clearCmd()
    except:
        print('Book: ', title, ' does not exist in Database')

#update the current book
def updateBookCmd():
    global current
    global product

    try:
        cur.execute("select * from book")
        currentBook = cur.fetchall()[current]
        isbn = currentBook[0]
        title = currentBook[1]
        newTitle = entry3.get()
        newSynopsis = entry4.get()
        newAuthor = entry5.get()
        newYear = int(entry6.get())
        newCategory = categoryTypeVar.get()
        rating = float(entry9.get())
        count = int(entry8.get())

        cur.execute("Update book set title = ?, synopsis = ?, author = ?, publicationYear = ?, category = ?, rating = ?, count = ? where isbn = ?",
                    [newTitle, newSynopsis, newAuthor, newYear, newCategory, rating, count, isbn])

        con.commit()
        display(current)
    except:
        print('Book: ' + title + 'does not exist in database')


#update the rating of the current book
def updateRatingCmd():
    global current
    global product
    cur.execute("select * from book")
    currentBook=cur.fetchall()[current]
    title=currentBook[1]
    count=currentBook[7]
    curr_rating=float(currentBook[6])
    newRating = int(ratingTypeVar.get())

    cur.execute("Update book set count=count + 1 where title = \'"+title +"\'")
    newAverage = ( (count*curr_rating + newRating))/(count+1)
    newAverage = newAverage.__round__(3)
    cur.execute("Update book set rating=\'" + str(newAverage) + "\' where title = \'" + title + "\'")
    con.commit()
    display(current)

#display the next book
def nextCmd():
    global current
    cur.execute("select * from book")
    allBooks=cur.fetchall()
    if (current<(len(allBooks)-1) ):
        current += 1
        display(current)

#display the previous book
def prevCmd():
    global current
    if (current > 0):
        current -= 1
        display(current)


# ----- Menu Event Handling -----------

#quit the application
def closeCmd():
    exit()

#clear all the inputs
def clearCmd():
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)
    entry5.delete(0, END)
    entry6.delete(0, END)
    categoryTypeVar.set("Fiction")
    entry8.delete(0 ,END)
    entry8.insert(END, 0)
    entry9.delete(0, END)
    entry9.insert(END, 0)

#create new book and save into db
def insertCmd():
    isbn = entry2.get()
    title = entry3.get()
    synopsis = entry4.get()
    author = entry5.get()
    year = int(entry6.get())
    category = categoryTypeVar.get()
    rating = float(entry9.get())
    count = int(entry8.get())

    newBook = [

        (isbn, title, synopsis, author, year, category, rating, count), ]

    cur.executemany("INSERT INTO book VALUES(?, ?, ?,?,?,?,?,?)", newBook)

    cur.execute("select * from book")
    allBooks = cur.fetchall()
    display(len(allBooks)-1)
    con.commit()

#-----------End of Event Handling


#=======================================================
# Menu to Add New Book
menu1 = Menu(window) #MenuBar
window.config(menu=menu1)
subm1=Menu(menu1)  #Menu
menu1.add_cascade(label="Admin", menu=subm1)
subm1.add_command(label="Update Book", font=("arial", 11, "bold"), command=updateBookCmd)
subm1.add_command(label="Delete Book", font=("arial", 11, "bold"), command = deleteCurrentCmd)   # menu item
subm1.add_command(label="Close", font=("arial", 11, "bold"), command = closeCmd)

#======= End of Menu Definition ============================


frame = Frame(window, width=200, height=200)
frame.place(x=10,y=80)

label1 = Label(window, text="Book Application", fg="blue",bg="yellow", font=("arial", 16, "bold"))
label1.place(x=90, y=30)                            # place on screen


label2 = Label(frame, text="ISBN", fg="blue",width=15, font=("arial", 10, "bold"))   #
label2.grid(row=0, column=0, sticky=W+E)

entry2 = Entry(frame)
entry2.insert(END, '0')
entry2.grid(row=0, column=1, sticky=W+E)

label3 = Label(frame, text="Title", fg="blue",width=15, font=("arial", 10, "bold"))   #
label3.grid(row=1, column=0, sticky=W+E)

entry3 = Entry(frame)
entry3.insert(END, '0')
entry3.grid(row=1, column=1, sticky=W+E)

label4 = Label(frame, text="Synopsis", fg="blue",width=15, font=("arial", 10, "bold"))   #
label4.grid(row=2, column=0, sticky=W+E)

entry4 = Entry(frame)
entry4.insert(END, '0')
entry4.grid(row=2, column=1, sticky=W+E)

label5 = Label(frame, text="Author", fg="blue",width=15, font=("arial", 10, "bold"))   #
label5.grid(row=3, column=0, sticky=W+E)

entry5 = Entry(frame)
entry5.insert(END, '0')
entry5.grid(row=3, column=1, sticky=W+E)


label6 = Label(frame, text="Publication Year", fg="blue",width=15, font=("arial", 10, "bold"))   #
label6.grid(row=4, column=0, sticky=W+E)

entry6 = Entry(frame)
entry6.insert(END, '0')
entry6.grid(row=4, column=1, sticky=W+E)

label7 = Label(frame, text="Category", fg="blue",width=15, font=("arial", 10, "bold"))   #
label7.grid(row=5, column=0, sticky=W+E)

list1=['Fiction','Non-Fiction']
categoryTypeVar = StringVar()
combo1= OptionMenu(frame, categoryTypeVar, *list1)
categoryTypeVar.set("Fiction")
combo1.grid(row=5,column=1, sticky=W+E)

label8 = Label(frame, text="No. of Ratings", fg="blue",width=15, font=("arial", 10, "bold"))   #
label8.grid(row=6, column=0, sticky=W+E)

entry8 = Entry(frame)
entry8.insert(END, '0')
entry8.grid(row=6, column=1, sticky=W+E)

label9 = Label(frame, text="Average Rating", fg="blue",width=15, font=("arial", 10, "bold"))   #
label9.grid(row=7, column=0, sticky=W+E)

entry9 = Entry(frame)
entry9.insert(END, '0')
entry9.grid(row=7, column=1, sticky=W+E)

#---------------------------

labelBlank = Label(frame, text=" ", fg="blue",width=15, font=("arial", 10, "bold"))   #
labelBlank.grid(row=10, column=0, columnspan=2,sticky=W+E)

button5 = Button(frame, text="Next", fg="black", font=("arial", 10, "bold"), command=nextCmd)
button5.grid(row=11, column=0, sticky=W+E)

button6 = Button(frame, text="Prev", fg="black", font=("arial", 10, "bold"), command=prevCmd)
button6.grid(row=11, column=1, sticky=W+E)

button7 = Button(frame, text="Clear", fg="black", font=("arial", 10, "bold"), command=clearCmd)
button7.grid(row=12, column=0, sticky=W+E)

button8 = Button(frame, text="InsertItem", fg="black", font=("arial", 10, "bold"), command=insertCmd)
button8.grid(row=12, column=1, sticky=W+E)

button11 = Button(frame, text="Add Rating", fg="black", font=("arial", 10, "bold"), command=updateRatingCmd)
button11.grid(row=15, column=0, sticky=W+E)

list11=['1','2','3','4','5']
ratingTypeVar = StringVar()
combo11= OptionMenu(frame, ratingTypeVar, *list11)
ratingTypeVar.set("3")
combo11.grid(row=15,column=1, sticky=W+E)

button13 = Button(frame, text="Display Full Synopsis", fg="black", font=("arial", 10, "bold"), command=displaySynopsis)
button13.grid(row=16, column=0, columnspan=2, sticky=W+E)

labelBlank2 = Label(frame, text=" ", fg="blue",width=15, font=("arial", 10, "bold"))   #
labelBlank2.grid(row=17, column=0, columnspan=2,sticky=W+E)

button12 = Button(frame, text="Display All Books", fg="black", font=("arial", 10, "bold"), command=displayAll)
button12.grid(row=18, column=0, columnspan=2, sticky=W+E)


button14 = Button(frame, text="Display By Title", fg="black", font=("arial", 10, "bold"), command=cmdTitleDisplay)
button14.grid(row=19, column=0, columnspan=1, sticky=W+E)

entry10 = Entry(frame)
entry10.grid(row=19, column=1, sticky=W+E)

button15 = Button(frame, text="Display By Author", fg="black", font=("arial", 10, "bold"), command=cmdAuthorDisplay)
button15.grid(row=20, column=0, columnspan=1, sticky=W+E)

entry11 = Entry(frame)
entry11.grid(row=20, column=1, sticky=W+E)

button16 = Button(frame, text="Display By Publication Year", fg="black", font=("arial", 10, "bold"), command=cmdYearDisplay)
button16.grid(row=21, column=0, columnspan=1, sticky=W+E)

yearTypeVar = StringVar()
list15=[2022,2021,2020,2019,2018,2017,2016,2015,2014,2013]
combo15= OptionMenu(frame, yearTypeVar, *list15)
yearTypeVar.set(2022)
combo15.grid(row=21,column=1, sticky=W+E)

button17 = Button(frame, text="Display By Category", fg="black", font=("arial", 10, "bold"), command=cmdCategoryDisplay)
button17.grid(row=22, column=0, columnspan=1, sticky=W+E)

catTypeVar = StringVar()
list16=['Fiction', 'Non-Fiction']
combo16= OptionMenu(frame, catTypeVar, *list16)
catTypeVar.set('Fiction')
combo16.grid(row=22,column=1, sticky=W+E)

button18 = Button(frame, text="Display By Rating", fg="black", font=("arial", 10, "bold"), command=cmdRatingDisplay)
button18.grid(row=23, column=0, columnspan=1, sticky=W+E)

list17=['1','2','3','4','5']
ratingTypeVar = StringVar()
combo17= OptionMenu(frame, ratingTypeVar, *list17)
ratingTypeVar.set("5")
combo17.grid(row=23,column=1, sticky=W+E)


display(0)


mainloop()