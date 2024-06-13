Trabajo Practico para Programacion sobre redes

Tomas Cabrera Farias


Funcionalidad de ?: Si el server recibe "?" se devolvera al cliente un mensaje con las funcionalidades del programa.


Que hace "server.py":

Implementacion de un servidor TCP que:

    Acepta conexiones entrantes de clientes.
    Permite la comunicación entre el servidor y los clientes.
    Difunde mensajes a todos los clientes si el mensaje comienza con '#'.
    Finaliza la conexión si el cliente envía "logout".
    Mantiene un registro de los clientes conectados y muestra la cantidad de conexiones activas.
    

Que hace "cliente.py":

Implementacion de un cliente TCP que:

    Se conecta a un servidor en la dirección IP y puerto especificados.
    Recibe mensajes del servidor en un hilo separado y los imprime.
    Lee la entrada del usuario y envía mensajes al servidor.
    Finaliza la conexión si el usuario escribe "logout".
