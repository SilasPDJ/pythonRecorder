import tkinter as tk
from tkinter import filedialog, messagebox
from os import path
from utils import MyMouseKeyboard
import time
import threading
from functools import partial

import pyautogui as pygui

class Application(tk.Frame):

    class MyButton(tk.Button):
        def __init__(self, *args, **kwargs):
            # tk.Button.__init__(self, *args, **kwargs)
            tk.Button.__init__(self, *args, **kwargs)

    class Widgets(tk.Menu):
        def __init__(self, *args, **kwargs):
            # tk.Button.__init__(self, *args, **kwargs)
            tk.Menu.__init__(self, *args, **kwargs)

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        menubar = self.Widgets()
        menubar.add_command(label='File')
        menubar.add_command(label='quit', command=root.quit)
        master.config(menu=menubar)

        bt = self.MyButton(fg='yellow', bg='blue')
        bt["text"] = 'SALVAR COMO'
        bt["command"] = lambda: self.start(self.dialog_select_arq)
        bt.pack(side="left")

        bt = self.MyButton(fg='red', bg='yellow')
        bt["text"] = 'Selecione arquivo'
        bt["command"] = lambda: self.start(self.dialog_select_arq)
        bt.pack(side="top")

        bt = self.MyButton(fg='black', bg='red')
        bt["text"] = 'GRAVAR'
        bt["command"] = lambda: self.start(self.gravando)
        bt.pack(side="top")
        # self.create_widgets()

        bt = self.MyButton(fg='black', bg='green')
        bt["text"] = 'REPRODUZIR'
        bt["command"] = lambda: self.start(self.executa)
        bt.pack(side="top")

    # threads
    def refresh(self):
        self.master.update()
        self.master.after(1000, self.refresh)

    def start(self, target):
        self.refresh()
        threading.Thread(target=target).start()
    # #######

    def mk_kboard_instance(self, select=False):
        try:
            narq = self.arq0atual
        except AttributeError:
            if select:
                narq = self.dialog_select_arq()
            else:
                narq = self.criauto_arq()
        print('narq: ')
        dale = MyMouseKeyboard(narq)
        return dale

    def mk_fld(self, fld):
        try:
            self.arq0atual_label.pack_forget()
        except (AttributeError, NameError):
            pass
        if fld == '':
            fld = self.criauto_arq()

        fld_resume = fld.replace(fld[3:len(fld) - int(len(fld)/2)], '...')
        self.arq0atual_label = tk.Label(text=f"arquivo atual: {fld_resume}")
        self.arq0atual_label.pack()
        self.arq0atual = fld

    def criauto_arq(self):
        fld = str(time.time()).replace('.', '')
        fld += '.txt'
        return fld

    #  -------------------------------botões
    def dialog_select_arq(self):
        fld0 = filedialog.askopenfilename(defaultextension='txt', filetypes=(('text files', 'txt'), ), initialdir=path.dirname(__file__))

        fld = f'{fld0}.txt' if path.splitext(fld0)[1] == '' else fld0
        self.mk_fld(fld)
        return fld

    def dialog_save_arq(self):
        fld0 = filedialog.asksaveasfilename(title="Salve a gravação", filetypes=(('text files', 'txt'), ))

        fld = f'{fld0}.txt' if path.splitext(fld0)[1] == '' else fld0
        self.mk_fld(fld)
        return fld

    def gravando(self):
        dale = self.mk_kboard_instance()
        dale.listen()
        dale.backup()

    def executa(self):
        dale = self.mk_kboard_instance(select=True)
        dale.playitbackup()
        messagebox.showinfo('FIM!!!', f'Arquivo {self.arq0atual} EXECUTADO COM SUCESSO. [enter] para continuar')

root = tk.Tk()
root.resizable(True, True)
rx, ry = pygui.getActiveWindow().center
root.geometry(f'250x100+{rx}+{ry}')

root.wm_iconposition(rx, ry)
app = Application(root)

app.mainloop()
