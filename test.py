from tkinter import *

class App(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.widgets()

    def widgets(self):
        menubar = Menu(root)
        menubar.add_command(label = 'File')
        menubar.add_command(label = 'quit', command = root.quit)
        root.config(menu = menubar)

root = Tk()
root.title('Menubar')
app = App(root)
root.mainloop()