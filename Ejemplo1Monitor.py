import threading
import random
import time
import logging
import queue

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

# Monitor (clase)

class colaMonitor():
# Variables locales (privadas) o permanentes (static) - Recursos
    _cola = None
    _consumiendo = 0
    _mutex = threading.RLock()
    _maxConsumidores = threading.Condition(_mutex)
    _item = 0
    _colaNoVacia = threading.Condition(_mutex)
    _colaNoLlena = threading.Condition(_mutex)

# Código de Inicialización (constructor)
    def __init__(self, size = 0):
        self._cola = queue.Queue(size)
        self.size = size

# Procedimientos Internos (privados)
## Regiones Críticas Condicionales para extraer e insertar
    def _extraer(self):
        with self._mutex:
            #Chequea y espera condición "Cola No Vacia"
            while self._cola.empty():
                self._colaNoVacia.wait()
            #Región Crítica
            _item = self._cola.get(block=False)
            #Fin Región Crítica

            #Notifica a hilos en espera que el estado del objeto cambió (se extrajo un elemento)
            self._colaNoLlena.notify_all()
            return _item

    def _insertar(self, valor):
        with self._mutex:
            #Chequea y espera condición "Cola No Llena"
            while self._cola.qsize() == self.size:
                self._colaNoLlena.wait()

            #Región Crítica
            self._cola.put(valor, block=False)
            #Fin Región Crítica

            #Notifica a hilos en espera que el estado del objeto cambió (se insertó un elemento)
            self._colaNoVacia.notify_all()

    def _extraerLista(self, lista, num_items):
        with self._mutex:
            for k in range (num_items):
                lista.append(self._extraer())


# Procedimientos exportados (publicos) - Todos con exclusión mútua (synchronized)

#Region Critica Condicional Max consumidores
    def extraer(self, lista, num_items):
        with self._mutex:
            #Chequea y espera condición: maximo 2 consumidores simultaneos
            while self._consumiendo == 2:
                self._maxConsumidores.wait()

            #Actualiza estado del objeto (nuevo consumidor activo)
            self._consumiendo += 1

            #Region Crítica
            self._extraerLista(lista, num_items)
            #Fin Region Critica

            #Actualiza estado del objeto y notifica a hilos en espera por la condición
            self._consumiendo -= 1
            self._maxConsumidores.notify_all()

#Región Crítica Productor (no es condicional)
    def insertar(self, valor):
        with self._mutex:
            self._insertar(valor)

class productor(threading.Thread):
    def __init__(self, cola):
        super().__init__()
        self.colaMon = cola

    def run(self):
        global valores
        while True:
            valor = random.randint(1,5)
            self.colaMon.insertar(valor)
      #      time.sleep(random.randint(0,1))

class consumidor(threading.Thread):
    def __init__(self, items, cola):
        super().__init__()
        self.medida = []
        self.items = items
        self.colaMon = cola

    def run(self):
        global consumiendo, max_consumidores
        while True:
            self.medida.clear()
            self.colaMon.extraer(self.medida, self.items)
            logging.info(f'medida {self.medida} promedio = {sum(self.medida)/self.items}')
            time.sleep(random.randint(0,5))

cola = colaMonitor(10)
hilos = []
for i in range(10):
    hilo = consumidor(random.randint(2,5), cola)
    hilos.append(hilo)

hilo = productor(cola)
hilos.append(hilo)

for hilo in hilos:
    hilo.start()


