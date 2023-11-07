from tkinter import *

def displayDialog(window, book_list):
    window2 = Toplevel(window)
    window2.geometry("1500x650")
    window2.title("Books")
    bookList = book_list


#============================================================
# Event Handling Methods

    def displayAll():
        for i in range(0, len(bookList)):
            line=''+bookList[i][0]
            line+= '\t\t\t'+bookList[i][1]
            line+= '\t\t\t\t\t' +bookList[i][3]
            line += '\t\t\t\t' +str(bookList[i][4])
            line += '\t\t\t' +bookList[i][5]
            line += '\t\t\t' + str(bookList[i][6])
            line+= '\n'+bookList[i][2]

            line += '\n\n'
            text.insert(END, line)


    def closeEvent():
        window2.destroy()

    button6 = Button(window2, text="Close", fg="black", font=("arial", 12, "bold"), command=closeEvent)
    button6.place(x=10, y=10)

    text = Text(window2, undo=True, height=34, width=182)
    text.place(x=20, y=60)

    displayAll()