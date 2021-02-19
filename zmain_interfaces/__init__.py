import tkinter as tk
from tkinter import filedialog, messagebox
from os import path
from utils import MyMouseKeyboard
import time
import threading
from functools import partial
import pyautogui as pygui

import subprocess
# subprocess.Popen is non-blocking
# subprocess.call is blocking


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
        menubar.add_command(label='Load File', command=lambda: self.start(self.dialog_open_arq))
        menubar.add_command(label='Save As File', command=lambda: self.start(self.dialog_save_arq))
        menubar.add_command(label='quit', command=master.quit)
        master.config(menu=menubar)
        """
        bt = self.MyButton(fg='black', bg='red')
        bt["text"] = 'GRAVAR'
        bt["command"] = lambda: self.start(self.gravando)
        bt.pack(side="top", anchor='w', fill=tk.X)
        """
        
        bt = self.MyButton(fg='black', bg='yellow')
        bt["text"] = 'Gera Novo Arquivo'
        bt["command"] = lambda: self.start(self.nova_gravacao)
        bt.pack(side="top", anchor='w', fill=tk.X)

        bt = self.MyButton(fg='black', bg='green')
        bt["text"] = 'REPRODUZIR'
        bt["command"] = lambda: self.start(self.executa)
        bt.pack(side="top", anchor='w', fill=tk.X)

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
                narq = self.dialog_open_arq()
            else:
                narq = self.mk_fld()

        dale = MyMouseKeyboard(narq)
        return dale

    def mk_fld(self, fld=None):
        try:
            self.arq0atual_label.pack_forget()
        except (AttributeError, NameError):
            pass
        if fld == '' or fld is None:
            fld = str(time.time()).replace('.', '')

        fld += f'.txt' if path.splitext(fld)[1] == '' else ''

        fld_path = path.abspath(fld)

        fld_resume = fld.replace(fld[3:len(fld) - int(len(fld)/2)], '...')
        print(path.dirname(path.abspath(fld)), 'print tche de teste', fld)
        self.arq0atual_label = tk.Button(text=f"arquivo atual: {fld_resume}",
                                         command=lambda: self.show_arq0(fld_path), bg='black', fg='white')

        self.arq0atual_label.pack()
        self.arq0atual = fld

        return self.arq0atual

    def show_arq0(self, to_file):

        texto = self.arq0atual_label["text"]
        try:
            open(to_file).close()
            subprocess.Popen(f'explorer /select,"{to_file}" ')
        except FileNotFoundError:
            # subprocess.Popen(f'explorer "{path.dirname(to_file)}"')
            # self.arq0atual_label["text"] = self.arq0atual_label["text"].replace('arquivo', 'GRAVE')
            self.arq0atual_label["text"] = 'GRAVAR PRIMEIRO'
        finally:
            if texto == 'GRAVAR PRIMEIRO':
                self.arq0atual_label['bg'] = 'red'
                self.arq0atual_label["text"] = 'GRAVANDO'
                self.gravando()
    #  -------------------------------botões
    def dialog_open_arq(self):
        fld0 = filedialog.askopenfilename(defaultextension='txt', filetypes=(('text files', 'txt'), ), initialdir=path.dirname(__file__))
        if fld0 == '':
            return None

        fld = self.mk_fld(fld0)
        return fld

    def dialog_save_arq(self):
        fld0 = filedialog.asksaveasfilename(title="Salve a gravação", filetypes=(('text files', 'txt'), ))
        fld = self.mk_fld(fld0)
        return fld

    def gravando(self):
        dale = self.mk_kboard_instance()
        dale.listen()
        dale.backup()

    def executa(self):
        dale = self.mk_kboard_instance(select=True)
        dale.playitbackup()
        messagebox.showinfo('FIM!!!', f'Arquivo {self.arq0atual} EXECUTADO COM SUCESSO. [enter] para continuar')

    def nova_gravacao(self):
        self.mk_fld(None)

def execute():
    root = tk.Tk()
    root.resizable(True, True)
    rx, ry = pygui.getActiveWindow().center
    root.geometry(f'250x100+{rx}+{ry}')

    root.wm_iconposition(rx, ry)
    app = Application(root)

    app.mainloop()
