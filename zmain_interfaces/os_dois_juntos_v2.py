from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Controller as MouseController
import pynput
import time
import pickle
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
import pyautogui as pygui
from win10toast import ToastNotifier
import tkinter as tk


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

    prossegue = True
    # Detecta key.pause [se foi pressionada]

    def __init__(self, file=None):
        self.file = file if file is not None else self.file
        self.geral = []
        pass
    # ---------------- MOUSE PART

    def on_move(self, x, y, *args):
        if not self.mousetimer:
            self.mousestart = time.time()
            self.mousetimer = True
            # not more necessary than that

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
        self.keytimer = False

        return round(end - self.keystart, 2)

    def get_time_taken4mouse(self):
        end = time.time()
        self.mousetimer = False

        return round(end - self.mousestart, 2)


    def listen(self):
        with MouseListener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll) as listener:
            with KeyboardListener(self.on_press, self.on_release) as listener:
                listener.join()
            try:
                listener.wait()
            finally:
                listener.stop()

    def playit(self):
        for dict_key in self.geral:
            tipo, el = list(dict_key.items())[0]
            if tipo == 'released':
                # tempo = list(dict_key.items())[1][1]
                tempo = dict_key['time_taken']
                time.sleep(tempo)
                self.kcontroller.release(el)
            elif tipo == 'pressed':
                # tempo = dict_key['time_taken']
                # time.sleep(tempo)
                self.kcontroller.press(el)
            elif tipo == 'clicked':
                myclick, move_to, pressed, tempo = dict_key.values()
                # print(myclick, move_to, pressed, tempo)
                # self.mcontroller.move(*move_to)

                if pressed:
                    pygui.click(*move_to, clicks=0, duration=tempo)
                    # time.sleep(2)
                    self.mcontroller.press(myclick)
                    # self.mcontroller.click(myclick)
                else:
                    pygui.click(*move_to, clicks=0, duration=1)
                    self.mcontroller.release(myclick)
            else:
                pass

    @staticmethod
    def press_keys_b4(*keys: str):
        from keyboard import is_pressed
        """
        :param keys: any key you wish
        :return:
        """
        while True:
            for key in keys:
                if is_pressed(key):
                    if is_pressed(key):
                        return key
                else:
                    pass
                    # print(key)


times = 100
tosleep = 4
# Fazer o GUI do times


toaster = ToastNotifier()
toaster.show_toast("Pressione F8 para iniciar, depois parar e executar",
"Python is 10 seconds awsm!",
# icon_path="custom.ico",
duration=2)

a = MyMouseKeyboard()

a.listen()
# l = a.press_keys_b4('f8')
# print(l)
for i in range(times):
    a.playit()
    time.sleep(tosleep)

