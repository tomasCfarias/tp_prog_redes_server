import sys
import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 12345
BUFFER_SIZE = 20
MESSAGE = "Hola Mundo!"

if len(sys.argv) >= 2:
    TCP_IP = sys.argv[1]

if len(sys.argv) >= 3:
    MESSAGE = sys.argv[2]

print("[CLIENTE] Iniciando")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("[CLIENTE] Conectando")
s.connect((TCP_IP, TCP_PORT))
print(f"[CLIENTE] Soy el cliente: \"{s.getsockname()}\"")
print(f"[CLIENTE] Enviando datos: \"{MESSAGE}\"")
s.send(MESSAGE.encode('utf-8'))
print("[CLIENTE] Recibiendo datos del SERVIDOR")
msg = ''
fin_msg = False
datos = bytearray()
while not fin_msg:
    recvd = s.recv(BUFFER_SIZE)
    datos += recvd
    print(f"[CLIENTE] Recibidos {len(recvd)} bytes")
    if b'\n' in recvd:
        msg = datos.rstrip(b'\n').decode('utf-8')
        fin_msg = True
print(f"[CLIENTE] Recibidos en total {len(datos)} bytes")
print(f"[CLIENTE] Datos recibidos en respuesta del SERVIDOR: \"{msg}\"")
print("[CLIENTE] Cerrando conexión con el SERVIDOR")
s.close()

print("[CLIENTE] Fin")
