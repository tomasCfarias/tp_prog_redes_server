import sys
import socket
import threading

# Configuración de la dirección IP y puerto del servidor
TCP_IP = '127.0.0.1'
TCP_PORT = 12345
BUFFER_SIZE = 1024  # Tamaño del búfer para la recepción de datos
MESSAGE_DELIMITER = b'\n'  # Delimitador de mensajes

# Permitir pasar la IP del servidor como argumento
if len(sys.argv) >= 2:
    TCP_IP = sys.argv[1]

# Recibe mensajes del servidor y los imprime.
def recibir_mensajes(sock):
    while True:
        try:
            buffer_datos = bytearray()  # Buffer para acumular datos recibidos
            while True:
                recibido = sock.recv(BUFFER_SIZE)  # Recibir datos del servidor
                
                if not recibido:
                    break
                buffer_datos += recibido
                
                if MESSAGE_DELIMITER in recibido:
                    mensaje = buffer_datos.rstrip(MESSAGE_DELIMITER).decode('utf-8')
                    print(f"{mensaje}")
                    
                    if mensaje.lower() == "logout":  # Finalizar la conexión si se recibe "logout"
                        print("[CLIENTE] Desconectando del servidor")
                        sock.close()  # Cerrar la conexión con el servidor
                        return
                    
                    buffer_datos.clear()
        except ConnectionError:
            print("[CLIENTE] Error de conexión")
            break

# Inicia el Cliente TCP y se conecta al servidor
def iniciar_cliente():
    print("[CLIENTE] Iniciando")
   
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente_socket:
        print("[CLIENTE] Conectando")
        cliente_socket.connect((TCP_IP, TCP_PORT))  # Conectarse al servidor
        print(f"[CLIENTE] Conexión exitosa a {TCP_IP}:{TCP_PORT}")

        hilo_receptor = threading.Thread(target=recibir_mensajes, args=(cliente_socket,), daemon=True)
        hilo_receptor.start()  # Iniciar un hilo para recibir mensajes

        while True:
            mensaje = input()  # Leer entrada del usuario y enviarla al servidor
            cliente_socket.sendall((mensaje + '\n').encode('utf-8'))  # Enviar el mensaje

            if mensaje.lower() == "logout":  # Enviar "logout" y terminar la conexión
                break

if __name__ == "__main__":
    iniciar_cliente()
