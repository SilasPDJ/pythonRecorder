import time
from tkinter import Button
from functools import partial, partialmethod
from utils import MyMouseKeyboard
import pyautogui as pygui
import pickle
import tkinter as tk
import threading


class AppInit(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)


class Backend:
    def __init__(self):

        main = partial(MyMouseKeyboard)
        self.mmk = main()

        self.record = partial(self.mmk.listen)
        self.exec = partial(self.mmk.playit)


class MainApplication(Backend, AppInit):
    myprint = partial(print, 'teste partial ')
    can_reset = True

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        # Backend.__init__(self)

        # primeiro pai, o supper se refere
        super().__init__()
        # Agora eu entendi, é a mesma coisa do que usar o que tá em cima, mas o super simplifica para mais rápido

        self.parent = parent
        self.root = parent

        bt_gravar = self.button('Gravar')
        bt_exec = self.button('Finalizar e Executar')
        bt_pause = self.button('PAUSE', command=lambda bg=bt_gravar: (self.pause4while(), self.change_state(bg, bt_pause)))

        bt_pause['state'] = 'disabled'
        bt_gravar.configure(command=lambda be=bt_exec, bg=bt_gravar: (self.main_record(bg), self.change_state(bg),
                                                                      self.change_state(be) if be['state'] == 'disabled' else None,
                                                                      self.change_state(bt_pause)))
        # eu só to redeclarando o bt_execute, etc
        bt_exec.configure(command=lambda be=bt_exec, bg=bt_gravar: (self.main_exec(be), self.change_state(bg, be, bt_pause)))

        self.__pack(bt_gravar)
        self.__pack(bt_exec)
        self.__pack(bt_pause)

        self.menubar()

    # Elements and placements
    @staticmethod
    def __pack(el, x=50, y=10, fill='x'):
        el.pack(padx=x, pady=y, fill=fill)

    def button(self, text, command=None, fg='#fff', bg='#000',):
        bt = Button(self, text=text, command=lambda: self.start(command), fg=fg, bg=bg)
        return bt
    # Elements and placements

    def menubar(self):
        menubar = tk.Menu(self.parent)

        filemenu = tk.Menu(menubar)
        filemenu.add_command(label="Open", command=lambda: print('open'))
        filemenu.add_command(label="Save", command=lambda: print('save'))
        filemenu.add_command(label="Exit", command=lambda: print('exit'))

        menubar.add_cascade(label="File", menu=filemenu)

        self.parent.config(menu=menubar)

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

    def main_record(self, caller_bt):
        if self.can_reset:

            Backend.__init__(self)
            self.mmk.reset_geral()

        caller_bt['bg'] = 'red'
        self.start(self.record)

    def main_exec(self, caller_bt):
        pygui.hotkey('f8')
        self.start(self.mmk.backup_save())
        # para habilitar novamente a gravação

        caller_bt['bg'] = 'red'
        self.start(self.exec)

    def pause4while(self):
        pygui.hotkey('f8')

        self.can_reset = False

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