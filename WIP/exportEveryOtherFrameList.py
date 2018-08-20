import tkFileDialog
from Tkinter import *
import os

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = tkFileDialog.askdirectory()
    folder_path.set(filename)
    print(filename)

def writeF(e1, e2):
    global folder_path
    try:
        sFrame = int(e1.get())
        eFrame = int(e2.get())
    except:
        print 'input frame must be int'
    if eFrame - sFrame < 1:
        print 'end frame must be bigger than start frame'
        return 1
    folder = folder_path.get()
    if not os.path.isdir(folder):
        print 'please select a valid folder'
        return 1
    targetFile = '%s/frameRange%s_%s.txt'%(folder, sFrame, eFrame)
    
    tmpF=''
    for i in range(sFrame, eFrame, 2):
        if not i == sFrame:
            tmpF += ','
        tmpF += str(i)
    
    with open(targetFile, 'w') as f:
        f.write(tmpF)
    
    print 'Finish export every other frame from %s to %s'%(sFrame, eFrame)
    
root = Tk()
folder_path = StringVar()

lbl1 = Label(master=root,textvariable=folder_path)
lbl1.grid(row=0, column=1)
E1 = Entry(bd =2)
E1.grid(row=1, column=1)
E2 = Entry(bd =2)
E2.grid(row=1, column=2)
button2 = Button(text="Browse", command=browse_button)
button2.grid(row=0, column=3)
button3 = Button(text="OK", command=lambda:writeF(E1,E2))
button3.grid(row=1, column=3)
mainloop()
