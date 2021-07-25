import time
from tkinter import Button
from functools import partial, partialmethod
from utils import MyMouseKeyboard
import pyautogui as pygui

import tkinter as tk
import threading


class AppInit(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)


class Backend:
    def __init__(self):

        main = partial(MyMouseKeyboard)
        self.main = main()

        self.record = partial(self.main.listen)
        self.exec = partial(self.main.playit)


class MainApplication(Backend, AppInit):
    myprint = partial(print, 'teste partial ')

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        # Backend.__init__(self)

        # primeiro pai, o supper se refere
        super().__init__()
        # Agora eu entendi, é a mesma coisa do que usar o que tá em cima, mas o super simplifica para mais rápido

        self.parent = parent
        self.root = parent

        bt_gravar = self.button('Gravar')
        bt_exec = self.button('Executar')

        bt_gravar.configure(command=lambda be=bt_exec, bg=bt_gravar: (self.main_record(bg, be), self.change_state(bg)))

        # eu só to redeclarando o lb, nada de mais

        bt_exec.configure(command=lambda be=bt_exec, bg=bt_gravar: (self.main_exec(be), self.change_state(bg)))

        bt_parar = self.button('Parar', command=lambda: pygui.hotkey('f8'))
        bt_parar['state'] = 'disabled'

        self.__pack(bt_gravar)
        self.__pack(bt_exec)
        self.__pack(bt_parar)

    # Elements and placements
    @staticmethod
    def __pack(el, x=50, y=10, fill='x'):
        el.pack(padx=x, pady=y, fill=fill)

    def button(self, text, command=None, fg='#fff', bg='#000',):
        bt = Button(self, text=text, command=lambda: self.start(command), fg=fg, bg=bg)
        return bt
    # Elements and placements

    @staticmethod
    def change_state(*args):
        """
        :param args: elements [buttons]
        :return:
        """
        for bt in args:

            bt_state = bt['state']

            if bt_state == 'normal':
                bt['state'] = 'disabled'
            else:
                bt['state'] = 'normal'

    def main_record(self, caller_bt, be_check):

        Backend.__init__(self)
        self.main.reset_geral()

        caller_bt['bg'] = 'red'
        self.start(self.record)
        if caller_bt['state'] == 'normal':
            be_check['state'] = 'normal'
        else:
            print(caller_bt['state'])

    def main_exec(self, caller_bt):
        pygui.hotkey('f8')
        # para habilitar novamente a gravação
        caller_bt['bg'] = 'red'
        self.start(self.exec)

    # threading...
    def refresh(self):
        self.root.update()
        self.root.after(1000, self.refresh)

    def start(self, stuff):
        self.refresh()
        threading.Thread(target=stuff).start()
    # threading

if __name__ == "__main__":
    root = tk.Tk()
    # a = MainApplication(root)
    # a.pack(side="bottom", fill="both", expand=True)
    b = MainApplication(root)
    b.pack(side="top", fill="both", expand=True)

    root.geometry('500x500')

    root.mainloop()

times = 100
tosleep = 4
# Fazer o GUI do times


# a = MyMouseKeyboard()
# a.listen()

"""for i in range(times):
    a.playit()
    time.sleep(tosleep)
"""