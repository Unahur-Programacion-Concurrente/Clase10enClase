import time
import logging

from multiprocessing.pool import ThreadPool

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

def super_task(a, b):
    time.sleep(1)     # Simulamos una tarea compleja.
    for a in range(5):
        logging.info('Terminamos la tarea compleja!!\n')
        time.sleep(2)


if __name__ == '__main__':
    print('Creamos un pool  con 2 threads')

    executor = ThreadPool(processes=2)

    # Programamos y ejecutamos 4 tareas de forma concurrente
    # Al solo existir 2 threads estas 2 tareas se ejecutarán primero
    executor.apply_async(super_task, args=(10, 20))
    executor.apply_async(super_task, args=(10, 20))

    # Al solo existir 2 threads estas 2 tareas se ejecutarán después
    executor.apply_async(super_task, args=(10, 20))
    executor.apply_async(super_task, args=(10, 20))

    executor.close()
    executor.join()

