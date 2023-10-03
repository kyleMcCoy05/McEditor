from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import ttkbootstrap as ttk

fileName = 'Untitled'
NAME = '<McEditor>'

appName = f"{fileName} - {NAME}"

def changeMode():
    if cb.get() == 1:
        style.theme_use('darkly')
    elif cb.get() == 0:
        style.theme_use('pulse')

def findFileName(dir):
    global appName
    ext = ['.txt',
           '.py']
    dir = dir.split('/')
    
    for i in dir:
        if i.endswith('.txt') or i.endswith('.py'):
            name = i

    for x in ext:
        name = name.removesuffix(x)
    
    appName = f"{name} - {NAME}"
    return name

def newFile(event = None):
    global fileName

    e = None

    if text.get(0.0, END) != "\n":
        result = askquestion("Save File", "Do you want to save this file?")
        if result == "yes":
            e = saveFile()
    
    if e != 'error':
        fileName = "Untitled"
        text.delete(0.0, END)

    appName = f"{fileName} - {NAME}"

    root.title(appName)
    root.update()

def saveFile(event = None):
    global fileName
    if fileName == 'Untitled':
        e = saveAs()
        if e == 'error':
            return e
    t = text.get(0.0, END)
    f = open(file='Files/'+fileName+'.txt', mode='w')
    f.write(t)
    fileName = findFileName(f.name)
    f.close()

    root.title(appName)
    root.update()

def saveAs(event = None):
    global fileName

    files = [
            ('All Files', '.*'), 
            ('Text Document', '.txt'),
            ('Python Files', '.py')
            ]
    
    f = asksaveasfile(
        defaultextension=files[1][1], 
        filetypes=files, 
        initialdir="Files", 
        initialfile=f'{fileName}',
        title="Save As")
    
    t = text.get(0.0, END)

    try:
        f.write(t.rstrip())

        fileName = findFileName(f.name)
    except:
        showerror("Save Error", "Unabe to save file...")
        return 'error'
        # print('\033[31m'+"Error - Unable to save file...", '\033[0m')

    root.title(appName)
    root.update()

def openFile(event = None):
    global fileName
    f = askopenfile(initialdir="Files", mode='r', title="Open")
    t = f.read()
    text.delete(0.0, END)
    text.insert(0.0, t)

    fileName = findFileName(f.name)

    root.title(appName)
    root.update()

def close(event = None):
    root.quit()

root = ttk.Window(
    title=appName,
    size=(1000, 600),
    resizable=(True, True),
    scaling= 2,
    iconphoto="icon.ico"
)

style = ttk.Style('darkly')

cb = IntVar(value=1)

text = Text(root, width=1000, height=600, wrap=['word'])
text.pack()

menuBar = Menu(root)

fileMenu = Menu(menuBar, tearoff=0)
fileMenu.add_command(label='Open', command=openFile)
fileMenu.add_command(label='New', command=newFile)
fileMenu.add_command(label='Save', command=saveFile)
fileMenu.add_command(label='Save As', command=saveAs)
fileMenu.add_separator()
fileMenu.add_checkbutton(label="Dark Mode", 
                         command=changeMode, 
                         onvalue=1, 
                         offvalue=0, 
                         variable=cb)
fileMenu.add_separator()
fileMenu.add_command(label="Quit", command=close)

menuBar.add_cascade(label="File", menu=fileMenu)

root.bind('<Control-s>', saveFile)
root.bind('<Control-n>', newFile)
root.bind('<Control-o>', openFile)
root.bind('<Control-q>', close)

root.config(menu=menuBar)
root.mainloop()