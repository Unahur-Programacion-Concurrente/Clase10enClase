from socket import AF_INET
from socket import SOCK_STREAM
from socket import socket
from concurrent.futures import ThreadPoolExecutor

def test_port_number(tupla):
    # crea y configura el socket
    with socket(AF_INET, SOCK_STREAM) as sock:
        # configurar timeout 100ms
        sock.settimeout(1)
        # la conexión puede fallar
        try:
            # intentar conectar
            sock.connect(tupla)
            # la conexión fue exitosa
            return True
        except:
            # si la conexión falla, ignorar
            return False

# escanea números de puerto en un host
def port_scan(host, ports):
    print(f'Scanning {host}...')
    # Crear el thred pool
    with ThreadPoolExecutor(len(ports)) as pool:
        # preparar los argumentos
        args = [(host,port) for port in ports]
        # enviar todas las tareas
        results = pool.map(test_port_number, args)
        # report results in order
        for port,is_open in zip(ports,results):
            if is_open:
                print(f'> {host}:{port} open')

# protejer el punto de entrada
if __name__ == '__main__':
    # definir host y numeros de port a escanear
    host = 'python.org'
    ports = range(1024)
    # testear los ports
    port_scan(host, ports)