import time
import logging

from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

def super_task(a, b):
    time.sleep(1)     # Simulamos una tarea compleja.
    for a in range(5):
        logging.info('Terminamos la tarea compleja!!\n')
        time.sleep(2)

if __name__ == '__main__':
    print('Creamos un pool  con 2 threads')

    executor = ThreadPoolExecutor(max_workers=2)

    # Programamos y ejecutamos 4 tareas de forma concurrente
    # Al solo existir 2 threads estas 2 tareas se ejecutarán primero
    executor.submit(super_task, 10, 20)
    executor.submit(super_task, 30, 40)

    # Al solo existir 2 threads estas 2 tareas se ejecutarán después
    executor.submit(super_task, 100, 200)
    executor.submit(super_task, 300,  400)
