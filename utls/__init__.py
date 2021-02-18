from pynput.keyboard import Key, Controller, Listener
import pynput
import time
import pickle


class MyKeyboard:
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
        with Listener(self.on_press, self.on_release) as listener:
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

"""
dale = MyKeyboard()
dale.listen()
dale.backup()
# dale.playit()
dale.playitbackup()
"""