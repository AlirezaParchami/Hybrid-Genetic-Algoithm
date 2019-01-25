import tkinter
import tkinter.filedialog

root = tkinter.Tk()
file = tkinter.filedialog.askopenfile(parent=root,mode='rb',title='Choose a file')
if file != None:
    data = file.read()
    file.close()
    print ("I got %d bytes from this file." % len(data))