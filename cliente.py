import sys
import socket
import threading

# Configuración de la dirección IP y puerto del servidor
TCP_IP = '127.0.0.1'
TCP_PORT = 12345
BUFFER_SIZE = 1024  # Tamaño del búfer para la recepción de datos
MESSAGE_DELIMITER = b'\n'  # Delimitador de mensajes

socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Permitir pasar la IP del servidor como argumento
if len(sys.argv) >= 2:
    TCP_IP = sys.argv[1]

# Recibe mensajes del servidor y los imprime.
def recibir_mensajes(sock): # Conexión del socket con el servidor
    while True:
        try:
            data = bytearray()  # Buffer para acumular datos recibidos
            while True:
                recvd = sock.recv(BUFFER_SIZE)  # Recibir datos del servidor
                if not recvd:
                    break
                data += recvd
                if MESSAGE_DELIMITER in recvd:
                    mensaje = data.rstrip(MESSAGE_DELIMITER).decode('utf-8')
                    print(f"[CLIENTE] Se envio: {mensaje}")
                    if mensaje.lower() == "logout":  # Finalizar la conexión si se recibe "logout"
                        print("[CLIENTE] Desconectando del SERVER")
                        sock.close() # Cerrar la conexión con el servidor
                        return
                    data.clear()
        except ConnectionError:
            print("[CLIENTE] Error de conexión")
            break
        except Exception as e:
            print(f"[CLIENTE] Error inesperado: {e}")
            break


# Inicia el Cliente TCP y se conecta al servidor
def iniciar_cliente():
    print("[CLIENTE] Iniciando")

    with socket_cliente as s:
        print("[CLIENTE] Conectando")
        s.connect((TCP_IP, TCP_PORT))  # Conectarse al servidor
        print(f"[CLIENTE] Conexion exitosa a {TCP_IP}:{TCP_PORT}")

        receiver_thread = threading.Thread(target=recibir_mensajes, args=(s,), daemon=True)
        receiver_thread.start()  # Iniciar un hilo para recibir mensajes

        while True:
            mensaje = input()  # Leer entrada del usuario y enviarla al servidor
            if mensaje.lower() == "logout":  # Enviar "logout" y terminar la conexión
                s.sendall((mensaje + '\n').encode('utf-8'))
                break
            s.sendall((mensaje + '\n').encode('utf-8'))



if __name__ == "__main__":
    iniciar_cliente()
