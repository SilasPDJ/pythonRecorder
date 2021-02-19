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

    stoprec_exe = False

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
        """
        :param select: if True, select the file
        :return: instance of MyMouseKeybaord
        """
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
        self.start(self.forget_arq0)
        if fld == '' or fld is None:
            fld = str(time.time()).replace('.', '')

        fld += f'.txt' if path.splitext(fld)[1] == '' else ''

        fld_path = path.abspath(fld)

        print(path.dirname(path.abspath(fld)), 'print tche de teste', fld)
        self.arq0atual_label = tk.Button(text=f"Start Recording",
                                         command=lambda: self.show_arq0(fld_path), bg='#fda321', fg='white')

        self.arq0atual_label.pack()
        self.arq0atual = fld

        return self.arq0atual

    def show_arq0(self, to_file):
        fld = to_file

        texto = self.arq0atual_label["text"]

        try:
            open(to_file).close()
            subprocess.Popen(f'explorer /select,"{to_file}" ')
        except FileNotFoundError:
            pass
        if texto == 'Start Recording':
            self.arq0atual_label['bg'] = 'red'
            self.arq0atual_label["text"] = 'Stop Recording'
            self.start(self.gravando)
            # ##################################
            # VOU ENVIAR AS CORDENADAS DO BOTÃO E QDO ELE FOR CLICADO, VAI ACABAR A THREAD
            # ################################
        elif texto == 'Stop Recording':
            fld_resume = fld.replace(fld[3:len(fld) - int(len(fld) / 2)], '...')
            self.arq0atual_label["text"] = fld_resume
            self.arq0atual_label['bg'] = 'black'
            self.stoprec()

    def forget_arq0(self):
        try:
            self.arq0atual_label.pack_forget()
        except (AttributeError, NameError):
            pass

    # QUANDO CLICAR NO BOTÃO

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

    def gravando(self, parou=False):
        dale = self.mk_kboard_instance()
        self.stoprec_exe = dale
        dale.listen()
        dale.backup()

    def stoprec(self):
        print(f'\033[1;31m STOP REC\033[m, {self.stoprec_exe}')
        if self.stoprec_exe:
            dale = self.stoprec_exe
            self.stoprec_exe.stopit()


    def executa(self):
        dale = self.mk_kboard_instance(select=True)
        try:
            dale.playitbackup()
        except FileNotFoundError:
            messagebox.showinfo('ERRO', 'Gere um novo arquivo primeiro!!!')
        else:
            messagebox.showinfo('FIM!!!', f'Arquivo {self.arq0atual} EXECUTADO COM SUCESSO. [enter] para continuar')

    def nova_gravacao(self):
        self.forget_arq0()
        self.mk_fld(None)

def execute():
    root = tk.Tk()
    root.resizable(True, True)
    rx, ry = pygui.getActiveWindow().center
    root.geometry(f'250x100+{rx}+{ry}')

    root.wm_iconposition(rx, ry)
    app = Application(root)

    app.mainloop()
