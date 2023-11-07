from tkinter import *

def displayDialog3(window, book):
    window3 = Toplevel(window)
    window3.geometry("1000x500")
    window3.title("Synopsis")
    book = book


#============================================================
# Event Handling Methods

    def displaySynopsis():
        for i in book:
            text.insert(END, i[0])


    def closeEvent():
        window3.destroy()

    button6 = Button(window3, text="Close", fg="black", font=("arial", 12, "bold"), command=closeEvent)
    button6.place(x=10, y=10)

    text = Text(window3, undo=True, height=26, width=119)
    text.place(x=20, y=60)

    displaySynopsis()