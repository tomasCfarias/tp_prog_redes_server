import threading
import socket

# Configuración de la dirección IP y puerto del servidor
TCP_IP = '127.0.0.1'  # Escuchar en todas las interfaces de red disponibles
TCP_PORT = 12345
BUFFER_SIZE = 1024  # Tamaño del búfer para la recepción de datos
MESSAGE_DELIMITER = b'\n'  # Delimitador de mensajes

clientes = {}  # Diccionario para almacenar las conexiones de clientes

# Envía mensajes a todos los clientes
def broadcast(mensaje, fuente_conn):
    for conn in clientes.values():
        if conn != fuente_conn:  # Evitar enviar el mensaje de vuelta al cliente origen
            conn.sendall(mensaje)  # Enviar el mensaje a los demás clientes

# Manejar la conexión con un cliente
def manejar_cliente(conn, addr):
    print(f"[SERVIDOR] Conectado satisfactoriamente con {addr}")
    clientes[addr] = conn  # Añadir el cliente al diccionario
    print(f"[SERVIDOR] Clientes conectados: {len(clientes)}")

    with conn:
        buffer_datos = bytearray()  # Buffer para acumular datos recibidos
        while True:
            try:
                recibido = conn.recv(BUFFER_SIZE)  # Recibir datos del cliente
                if not recibido:
                    break
                buffer_datos += recibido
                if MESSAGE_DELIMITER in recibido:
                    mensaje = buffer_datos.rstrip(MESSAGE_DELIMITER).decode('utf-8')
                    print(f"[SERVIDOR] {addr} dice: {mensaje}")
                    
                    if mensaje.lower() == "logout":  # Finalizar la conexión si el cliente envía "logout"
                        break
                    elif mensaje.startswith('#'):  # Difundir el mensaje a todos los clientes si empieza con "#"
                        broadcast(buffer_datos, conn)
                    elif mensaje == "?":  # Responder con un mensaje específico si el cliente envía "?"
                        respuesta = (
                            "-------------------------------------------------------------------------------------\n"
                            "Funcionalidades:\n"
                            "1. Si escribe '#' antes de un mensaje, ese mensaje se enviará a todos los clientes.\n"
                            "2. Si escribe 'logout', se desconectará del servidor.\n"
                            "-------------------------------------------------------------------------------------"
                        )
                        conn.sendall((respuesta + '\n').encode('utf-8'))  # Enviar respuesta al cliente
                    else:
                        conn.sendall(buffer_datos)  # Enviar el eco de vuelta al cliente
                    buffer_datos.clear()
            except ConnectionError:
                break
            except Exception as error:
                print(f"[SERVIDOR] Error: {error}")
                break

    print(f"[SERVIDOR] Desconectando {addr}")
    del clientes[addr]  # Remover el cliente del diccionario al desconectarse
    print(f"[SERVIDOR] Clientes conectados: {len(clientes)}")

# Inicia el Servidor TCP y espera conexiones entrantes
def iniciar_servidor():
    print("[SERVIDOR] Iniciando")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.bind((TCP_IP, TCP_PORT))  # Enlazar el socket a la dirección IP y puerto
        servidor.listen()  # Escuchar conexiones entrantes
        print(f"[SERVIDOR] Escuchando en el puerto {TCP_PORT}")

        while True:
            conn, addr = servidor.accept()  # Aceptar una nueva conexión
            print(f"[SERVIDOR] Conexión desde: {addr}")
            hilo = threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True)
            hilo.start()

if __name__ == "__main__":
    iniciar_servidor()
