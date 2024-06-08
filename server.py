import threading
import socket

# Configuración de la dirección IP y puerto del servidor
TCP_IP = '127.0.0.1'  # Escuchar en todas las interfaces de red disponibles
TCP_PORT = 12345
BUFFER_SIZE = 1024  # Tamaño del búfer para la recepción de datos
MESSAGE_DELIMITER = b'\n'  # Delimitador de mensajes

clientes = {}  # Diccionario para almacenar las conexiones de clientes

# Envia mensajes a todos los clientes
def broadcast(message, source_conn):
    for conn in clientes.values():
        if conn != source_conn: #Conexión del cliente que envió el mensaje
            conn.sendall(message) # Mensaje 

#Conexion con el cliente
def contacto_cliente(conn, addr):
    print(f"[SERVIDOR] Conectado satisfactoriamente con {addr}")
    clientes[addr] = conn  # Añadir el cliente al diccionario
    print(f"[SERVIDOR] Clientes conectados: {len(clientes)}")

    with conn:
        data = bytearray()  # Buffer para acumular datos recibidos
        while True:
            try:
                received = conn.recv(BUFFER_SIZE)  # Recibir datos del cliente
                if not received:
                    break
                data += received
                if MESSAGE_DELIMITER in received:
                    mensaje = data.rstrip(MESSAGE_DELIMITER).decode('utf-8')
                    print(f"[SERVIDOR]{addr} dice: {mensaje}  ")
                    if mensaje.lower() == "logout":  # Finalizar la conexión si el cliente envía "logout"
                        break
                    if mensaje.startswith('#'):  # Difundir el mensaje a todos los clientes si empieza con "#"
                        broadcast(data, conn)
                    elif mensaje == "?":  # Responder con un mensaje específico si el cliente envía "?"
                        respuesta = "Funcionalidades: Si escribe # antes de un mensaje, ese mensaje se enviará a todos los clientes"
                        "Si escribe logout se desconectará del server."
                        conn.sendall((respuesta + '\n').encode('utf-8')) # Transforma el string en bytes
                    else:
                        conn.sendall(data)  # Enviar el eco de vuelta al cliente
                    data.clear()
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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((TCP_IP, TCP_PORT))  # Enlazar el socket a la dirección IP y puerto
        s.listen()  # Escuchar conexiones entrantes
        print(f"[SERVIDOR] Escuchando {TCP_PORT}")
        while True:
            conn, addr = s.accept()  # Aceptar una nueva conexión y crear un hilo para manejarla
            print(f"[SERVIDOR] Se unio: {addr}")
            thread = threading.Thread(target=contacto_cliente, args=(conn, addr), daemon=True)
            thread.start()

if __name__ == "__main__":
    iniciar_servidor()
