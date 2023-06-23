import threading
import time
import random
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S',
                    level=logging.INFO)


# Monitor (clase)
class energiaMonitor():
    # Variables locales (privadas) o permanentes (static) - Recursos
    _energia = 0
    _mutex = threading.RLock()
    _maxMedidores = threading.Condition(_mutex)
    _hilosMidiendo = []
    # Código de Inicialización (constructor)
    def __init__(self, energia_inicial = 0):
        self._energia = energia_inicial

# Procedimientos Internos (privados) - Todos con exclusión mútua (synchronized)

# Procedimientos exportados (publicos) - Todos con exclusión mútua (synchronized)
    def incrementar(self, incremento = 1):
        with self._mutex:
            self._energia += incremento
            time.sleep(0.0001)

    def medir(self):
        with self._mutex:
            while len(self._hilosMidiendo) == 2 and threading.current_thread().name not in self._hilosMidiendo:
                self._maxMedidores.wait()
            if threading.current_thread().name not in self._hilosMidiendo:
                self._hilosMidiendo.append(threading.current_thread().name)
            else:
                self._hilosMidiendo.pop(self._hilosMidiendo.index(threading.current_thread().name))
                self._maxMedidores.notify_all()
            return self._energia


energia = energiaMonitor()

def generador():
    while True:
        energia.incrementar()
        time.sleep(random.randint(1, 2) / 100)

def medidor(iteraciones):
    for k in range(iteraciones):
        valor0 = energia.medir()
        logging.info(f'{threading.current_thread().name} esta midiendo')
        time.sleep(1)
        valor1 = energia.medir()
        logging.info(f'La potencia generada es {valor1 - valor0} Kw')
        time.sleep(2)

hilos = []


for k in range(2):
    hilos.append(threading.Thread(target=generador, name=f'Generador {k}'))

for k in range(10):
    hilos.append(threading.Thread(target=medidor, name=f'Medidor {k}', args=(4,)))

for hilo in hilos:
    hilo.start()

