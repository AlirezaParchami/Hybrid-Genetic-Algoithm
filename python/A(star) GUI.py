from tkinter import *
import tkinter.filedialog
def openfile():
    file = tkinter.filedialog.askopenfile(parent=window,mode='rb',title='Choose a file')
    if file != None:
        data = file.read()
        file.close()
        print("I got %d bytes from this file." % len(data))

window = Tk()
Button(window, text="Browse", width = 8, command=openfile()).grid(row = 0, column=0, sticky=W)
window.mainloop()
