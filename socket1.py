from socket import AF_INET
from socket import SOCK_STREAM
from socket import socket

def test_port_number(host, port):
    # crea y configura el socket
    with socket(AF_INET, SOCK_STREAM) as sock:
        # configurar timeout 100ms
        sock.settimeout(0.1)
        # la conexión puede fallar
        try:
            # intentar conectar
            sock.connect((host, port))
            # la conexión fue exitosa
            return True
        except:
            # si la conexión falla, ignorar
            return False

# escanea números de puerto en un host
def port_scan(host, ports):
    print(f'Scanning {host}...')
    # escanear puertos
    for port in ports:
        if test_port_number(host, port):
            print(f'> {host}:{port} abierto')

# protejer el punto de entrada
if __name__ == '__main__':
    # definir host y numeros de port a escanear
    host = 'python.org'
    ports = range(1024)
    # testear los ports
    port_scan(host, ports)