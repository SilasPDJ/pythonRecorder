import tkinter as tk
from tkinter import filedialog, messagebox
from os import path
import pickle
from utls import MyKeyboard
import time
import threading
from functools import partial


class Application(tk.Frame):

    class MyButton(tk.Button):
        def __init__(self, *args, **kwargs):
            tk.Button.__init__(self, *args, **kwargs)

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        bt = self.MyButton(fg='red', bg='yellow')
        bt["text"] = 'Selecione arquivo'
        bt["command"] = lambda: self.start(self.selec_arq)
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
        # self.create_widgets()

    # threads
    def refresh(self):
        self.master.update()
        self.master.after(1000, self.refresh)

    def start(self, target):
        self.refresh()
        threading.Thread(target=target).start()
    # #######

    def selec_arq(self):
        fld = filedialog.askopenfilename(defaultextension='txt', filetypes=(('text files', 'txt'), ), initialdir=path.dirname(__file__))
        self.mk_fld(fld)
        return fld

    def cria_arq(self):
        fld0 = filedialog.asksaveasfilename(title="Salve a gravação", filetypes=(('text files', 'txt'), ))

        fld = f'{fld0}.txt' if path.splitext(fld0)[1] == '' else fld0
        self.mk_fld(fld)
        return fld

    def mk_fld(self, fld):
        try:
            self.arq0atual_label.pack_forget()
        except (AttributeError, NameError):
            pass
        if fld == '':
            fld = str(time.time()).replace('.', '')
            fld += '.txt'
        fld_resume = fld.replace(fld[3:len(fld) - int(len(fld)/2)], '...')
        self.arq0atual_label = tk.Label(text=f"arquivo atual: {fld_resume}")
        self.arq0atual_label.pack()
        self.arq0atual = fld

    def mk_kboard_instance(self, select=False):
        try:
            narq = self.arq0atual
        except AttributeError:
            if select:
                narq = self.selec_arq()
            else:
                narq = self.cria_arq()
        print('narq: ')
        dale = MyKeyboard(narq)
        return dale

    def gravando(self):
        dale = self.mk_kboard_instance()
        dale.listen()
        dale.backup()

    def executa(self):
        dale = self.mk_kboard_instance(select=True)
        dale.playitbackup()
        messagebox.showinfo('FIM!!!', f'Arquivo {self.arq0atual} EXECUTADO COM SUCESSO. [enter] para continuar')


root = tk.Tk()
app = Application(master=root)
# app.MyButton(text="Testo").pack()

app.mainloop()
