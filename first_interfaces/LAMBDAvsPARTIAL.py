import threading
from tkinter import Tk
import tkinter as tk

from functools import partial
# lambda => anonymous
# partial => named and frozen


class Gui(tk.Frame):

    class MyButton(tk.Button):
        def __init__(self, *args, **kwargs):
            tk.Button.__init__(self, *args, **kwargs)

    def __init__(self, master=None):
        super().__init__(master)
        self.root = master
        command = partial(self.start, self.doingALotOfStuff)
        # self.MyButton(text="teste", command=lambda: self.start(self.doingALotOfStuff)).pack()
        self.MyButton(text="teste", command=command).pack()

    def doingALotOfStuff(self):
        from time import sleep
        while True:
            sleep(1)
            print(True)

    def refresh(self):
        self.root.update()
        self.root.after(1000, self.refresh)

    def start(self, target):
        self.refresh()
        threading.Thread(target=target).start()

#outside
GUI = Gui(Tk())
GUI.mainloop()