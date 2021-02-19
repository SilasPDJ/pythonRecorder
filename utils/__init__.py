from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Controller as MouseController
import pynput
import time
import pickle
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
import pyautogui as pygui


class MyMouseKeyboard:
    file = 'testsave.txt'

    kcontroller = KeyboardController()
    mcontroller = MouseController()
    live_time_program = time.time()

    keystart = time.time()
    mousestart = time.time()
    keytimer = False
    mousetimer = False

    # quando False, gera um novo contador time.time()
    # Lógica para detectar por quanto tempo uma tecla/click tá sendo pressionada/o

    def __init__(self, file=None):
        self.file = file if file is not None else self.file
        self.geral = []
        pass
    # ---------------- MOUSE PART

    def on_move(self, x, y):
        if not self.mousetimer:
            self.mousestart = time.time()
            self.mousetimer = True

    def on_click(self, x, y, button, pressed):
        print(f'clicking: x:{x}, y:{y}; {button}; {pressed}')
        appended = {"clicked": button, 'move_to': [x, y], 'pressed': pressed, 'time_taken': self.get_time_taken4mouse()}
        print(appended['time_taken'])
        self.geral.append(appended)

    def on_scroll(self, x, y, dx, dy):
        print('scrolling')

    # ---------------- MOUSE PART

    def on_press(self, key):

        if not self.keytimer:
            self.keystart = time.time()
            self.keytimer = True

        self.geral.append({"pressed": key})

    def get_time_taken(self):
        end = time.time()
        self.keytimer = False

        return round(end - self.keystart, 2)

    def get_time_taken4mouse(self):
        end = time.time()
        self.mousetimer = False

        return round(end - self.mousestart, 2)

    def on_release(self, key):
        pause_key = Key.pause
        appended = {"released": key, 'time_taken': self.get_time_taken()}
        self.geral.append(appended)
        print(appended['time_taken'])

        if pause_key is key or pause_key == key:
            return False

    def listen(self):
        with MouseListener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll) as listener:
            with KeyboardListener(self.on_press, self.on_release) as listener:
                listener.join()
            try:
                listener.wait()
            finally:
                listener.stop()

    def backup(self):

        # Appending...
        try:
            with open(self.file, 'rb') as rf:
                was = pickle.load(rf)
            with open(self.file, 'wb') as wf:
                novo = was
                novo += self.geral.copy()
                pickle.dump(novo, wf)

        except FileNotFoundError:
            with open(self.file, 'wb') as wf:
                novo = self.geral.copy()
                pickle.dump(novo, wf)

    def playit(self):
        for dict_key in self.geral:
            tipo, el = list(dict_key.items())[0]
            if tipo == 'released':
                # tempo = list(dict_key.items())[1][1]
                tempo = dict_key['time_taken']
                time.sleep(tempo)
                self.kcontroller.release(el)
            elif tipo == 'pressed':
                self.kcontroller.press(el)
            elif tipo == 'clicked':
                myclick, move_to, pressed, tempo = dict_key.values()
                # print(myclick, move_to, pressed, tempo)
                # self.mcontroller.move(*move_to)
                if pressed is True:
                    time.sleep(tempo)
                    pygui.click(*move_to)
                    # self.mcontroller.press(el, *move_to)

    def playitbackup(self):
        with open(self.file, 'rb') as rf:
            rp = pickle.load(rf)
        for dict_key in rp:
            print(dict_key)

            tipo, el = list(dict_key.items())[0]
            if tipo == 'released':
                # tempo = list(dict_key.items())[1][1]
                tempo = dict_key['time_taken']
                time.sleep(tempo)
                self.kcontroller.release(el)
            elif tipo == 'pressed':
                self.kcontroller.press(el)
            elif tipo == 'clicked':
                time.sleep(.25)
                myclick, move_to, pressed, tempo = dict_key.values()
                # print(myclick, move_to, pressed, tempo)
                # self.mcontroller.move(*move_to)
                if pressed is True:
                    time.sleep(tempo)
                    pygui.click(*move_to)
                    # self.mcontroller.press(el, *move_to)
        print('FIM.....')

    def stopit(self):
        self.kcontroller.press(Key.pause)
        self.kcontroller.release(Key.pause)


class MyKeyboardV001:
    from pynput.keyboard import Key, Controller, Listener
    import pynput
    import time
    import pickle
    file = 'testsave.txt'

    controller = Controller()
    live_time_program = time.time()

    start = time.time()
    ss_count = False
    # quando False, gera um novo contador time.time()
    # Lógica para detectar por quanto tempo uma tecla tá sendo pressionada

    prossegue = True
    # Detecta key.pause [se foi pressionada]

    def __init__(self, file):
        self.file = file
        self.geral = []

    def on_press(self, key):

        if not self.ss_count:
            self.start = time.time()
            self.ss_count = True
        if self.prossegue:
            self.geral.append({"pressed": key})

    def on_release(self, key):
        pause_key = Key.pause
        if key is pause_key and self.prossegue is False:
            self.prossegue = True
            print('Pode prosseguir')
        else:
            if key is pause_key:
                self.prossegue = False
                print('\033[1;31mPediu para parar, parou\033[m')
            elif self.prossegue is False:
                self.prossegue = False
            else:
                self.prossegue = True

            if key == Key.f8:
                return False
        if self.prossegue:

            appended = {"released": key, 'time_taken': self.get_time_taken()}
            self.geral.append(appended)
            print(appended['time_taken'])


    def get_time_taken(self):
        end = time.time()
        self.ss_count = False

        return round(end - self.start, 2)

    def listen(self):

        with KeyboardListener(self.on_press, self.on_release) as listener:
            listener.join()
        try:
            listener.wait()
        finally:
            listener.stop()
    """
    def playit(self):
        for dict_key in self.geral:
            tipo, tecla = list(dict_key.items())[0]
            if tipo == 'released':
                # tempo = list(dict_key.items())[1][1]
                tempo = dict_key['time_taken']
                time.sleep(tempo)
                self.controller.release(tecla)
            elif tipo == 'pressed':
                self.controller.press(tecla)
    """
    def backup(self):
        with open(self.file, 'wb') as wf:
            novo = self.geral.copy()
            pickle.dump(novo, wf)

    def playitbackup(self):
        with open(self.file, 'rb') as rf:
            rp = pickle.load(rf)
        for dict_key in rp:
            # input(dict_key)

            # """
            tipo, tecla = list(dict_key.items())[0]
            if tipo == 'released':
                tempo = dict_key['time_taken']
                time.sleep(float(tempo))
                self.controller.release(tecla)
            elif tipo == 'pressed':
                self.controller.press(tecla)
            # """

