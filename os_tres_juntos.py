import time
from tkinter import Button
from functools import partial, partialmethod
from utils import MyMouseKeyboard
import pyautogui as pygui
import pickle
import tkinter as tk
import threading
from tkinter import filedialog, messagebox


class AppInit(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)


class Backend:
    need2save = True
    can_reset = True

    file2save = 'custom.json'

    def __init__(self):

        main = partial(MyMouseKeyboard)
        self.mmk = main()

        self.record = partial(self.mmk.listen)
        self.exec = partial(self.mmk.playit)
        # dialogs

    def save_as(self):
        # if messagebox.askyesno('ATENÇÃO!!!', message='Deseja concluir a gravação?'):
        can_bsaved = True
        if not self.mmk.geral:
            can_bsaved = not messagebox.askyesno('ATENÇÃO!!!', message='Vamos gravar primeiro?')

        if can_bsaved:
            fl = filedialog.asksaveasfilename(title="Salve a gravação", defaultextension=('.txt',))
            self.file2save = fl

            self.mmk.backup_save(self.file2save)

    def open_file(self, bt_exec):
        filetypes = (
            ('txt files', '*.txt'),
            ('All files', '*.*')
        )
        # show the open file dialog
        self.mmk.backup_restore(filedialog.askopenfilename(filetypes=filetypes))
        # askfilename get only name, askfile full object

        self.can_reset = True
        self.need2save = False
        bt_exec['state'] = 'normal'


    @staticmethod
    def change_state(*args, change_to=None):
        """
        :param args: elements [buttons]
        :param change_to: Change state to [normal, disabled, ...], if None changes to opposite, 0 -> disabled, 1 -> normal
        :return:
        """
        for bt in args:
            bt_state = bt['state']
            if change_to is None:
                if bt_state == 'normal':
                    bt['state'] = 'disabled'
                else:
                    bt['state'] = 'normal'
            else:
                if str(change_to).lower().strip() == 'disabled' or str(change_to).lower().strip() == 'normal':
                    pass
                elif not isinstance(change_to, int):
                    print(f'{bt} em estado NORMLA')
                    change_to = 'normal'
                else:
                    change_to = 'disabled' if change_to == 0 else 'normal'

                bt['state'] = change_to


class MainApplication(Backend, AppInit):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        # Backend.__init__(self)

        # primeiro pai, o supper se refere
        super().__init__()
        # Agora eu entendi, é a mesma coisa do que usar o que tá em cima, mas o super simplifica para mais rápido

        self.parent = parent
        self.root = parent

        bt_gravar = self.button('Gravar')
        self.bt_exec = bt_exec = self.button('Finalizar e Executar')
        bt_pause = self.button('PAUSE', command=lambda bg=bt_gravar: (self.pause4while(), self.change_state(bg, change_to=1)))

        bt_pause['state'] = 'disabled'
        bt_gravar.configure(command=lambda be=bt_exec, bg=bt_gravar: (
            self.main_record(bg), self.change_state(bg, change_to='disabled'), self.change_state(be, bt_pause, change_to=1),
            self.change_state(bt_pause, change_to=1)))

        # eu só to redeclarando o bt_execute, etc
        bt_exec.configure(command=lambda be=bt_exec, bg=bt_gravar: (self.main_exec(be), self.change_state(be, bt_pause, change_to=0),
                                                                    self.change_state(bg, change_to=1)))
        self.change_state(bt_exec)

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
        def donothing():
            pass
        menubar = tk.Menu(self.parent)

        filemenu = tk.Menu(menubar, tearoff=0)
        # filemenu.add_command(label="New", command=donothing)
        filemenu.add_command(label="Open", command=lambda: self.open_file(self.bt_exec))
        filemenu.add_command(label="Save", command=donothing)
        filemenu.add_command(label="Save as...", command=self.save_as)
        filemenu.add_command(label="Close", command=donothing)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=donothing)

        editmenu.add_separator()

        editmenu.add_command(label="Cut", command=donothing)
        editmenu.add_command(label="Copy", command=donothing)
        editmenu.add_command(label="Paste", command=donothing)
        editmenu.add_command(label="Delete", command=donothing)
        editmenu.add_command(label="Select All", command=donothing)

        menubar.add_cascade(label="Edit", menu=editmenu)
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=donothing)
        helpmenu.add_command(label="About...", command=donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.parent.config(menu=menubar)

    def main_record(self, caller_bt):
        if self.can_reset:

            Backend.__init__(self)
            self.mmk.reset_geral()

        caller_bt['bg'] = 'red'
        self. need2save = True
        self.start(self.record)

    def main_exec(self, caller_bt):
        pygui.hotkey('f8')
        if self.need2save:
            self.save_as()
        time.sleep(1)
        # para habilitar novamente a gravação
        # self.mmk.backup_save(self.file2save)

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