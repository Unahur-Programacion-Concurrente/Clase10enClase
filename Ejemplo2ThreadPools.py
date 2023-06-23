import threading
import time
import random
import logging

#from concurrent.futures import ThreadPoolExecutor

from multiprocessing.pool import ThreadPool

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S',
                    level=logging.INFO)


# Monitor (clase)
class energiaMonitor():
    # Variables locales (privadas) o permanentes (static) - Recursos
    _energia = 0
    _mutex = threading.RLock()
    _numMedidores = 0
    _maxMedidores = threading.Condition(_mutex)
    _hilosMidiendo = []
    _ultimoHilo = 0
    # Código de Inicialización (constructor)
    def __init__(self, energia_inicial = 0):
        self._energia = energia_inicial
        self._estoyMidiendo = False

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

def task_generador():
    while True:
        energia.incrementar()
        time.sleep(random.randint(1, 2) / 100)

def task_medidor():
    while True:
        valor0 = energia.medir()
        logging.info(f'{threading.current_thread().name} esta midiendo')
        time.sleep(1)
        valor1 = energia.medir()
        logging.info(f'La potencia generada es {valor1 - valor0} Kw')
        time.sleep(2)

pool = ThreadPool(processes=5)


pool.apply_async(task_generador)
pool.apply_async(task_generador)

pool.apply_async(task_medidor)
pool.apply_async(task_medidor)
pool.apply_async(task_medidor)
pool.apply_async(task_medidor)
pool.apply_async(task_medidor)
pool.apply_async(task_medidor)


pool.close()
pool.join()