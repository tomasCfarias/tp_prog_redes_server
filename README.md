
# Trabajo Practico  SOCKETS

En este trabajo se crea un socket en un script llamado "server.py", el cual permite escuchar mensajes y distribuirlos a los scripts "clientes.py" conectados.

## Funcionalidad de "?" 
Si el server recibe "?" se devolvera al cliente un mensaje con las funcionalidades del programa.

## Que hace "server.py"

- Acepta conexiones entrantes de clientes.
- Permite la comunicación entre el servidor y los clientes.
- Difunde mensajes a todos los clientes si el mensaje comienza con '#'.
- Finaliza la conexión si el cliente envía "logout".
- Mantiene un registro de los clientes conectados y muestra la cantidad de conexiones activas.

## Que hace "cliente.py":

- Se conecta a un servidor en la dirección IP y puerto especificados.
- Recibe mensajes del servidor en un hilo separado y los imprime.
- Envía mensajes al servidor.
- Finaliza la conexión si el usuario escribe "logout".

## Alumno

- Tomas Cabrera Farias

