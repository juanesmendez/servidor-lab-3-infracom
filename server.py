import socket
import select
import pickle

HEADERSIZE = 10
IP = "127.0.0.1"
PORT = 1236
FILE_1 = "./files/prueba.pdf"
FILE_2 = ""

def createMessage(message):
    #Chequear el atributo message size, puede que esté incorrecto
    msg = {"messageSize": len(message.encode("utf-8")),
     "message": message.upper()}
    msg = pickle.dumps(msg)
    # Añadir header de 10 bytes
    messageHeader = f"{len(msg):<{HEADERSIZE}}".encode("utf-8")

    print(f"Message header: {messageHeader}")
    print(f"Message payload: {msg}")

    # Retornamos el header con el mensaje convertido en bytes
    print(f"Sending message '{messageHeader + msg}'")
    return messageHeader + msg


def receiveMessage(clientSocket):
    print("Receiving message from client...")
    try:
        # Desarmar header para saber el tamaño en bytes del mensaje
        messageHeader = clientSocket.recv(HEADERSIZE)
        print(f"Message header before: {messageHeader}")
        # Atrapo el tamaño en bytes del mensaje que se va a recibir
        messageLength = int(messageHeader.decode("utf-8").strip())
        print(f"Message header length: {messageLength}")
        # Se recibe el mensaje del socket
        message = clientSocket.recv(messageLength)
        print(f"Message payload: {message}")
        message = pickle.loads(message)

        print(f"Message received from client: {message}")
        print(message)
        return message
    except Exception as e:
        print('General error', str(e))


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serverSocket.bind((IP, PORT))
serverSocket.listen(5) # Listen to five connections

socketsList = [serverSocket]

clients = {}

while True:
    readSockets, writingSockets, exceptionSockets = select.select(socketsList, [], socketsList)
    for notifiedSocket in readSockets:
        if notifiedSocket == serverSocket:
            clientSocket, clientAddress = serverSocket.accept()
            print(str(clientSocket))
            print(f"Accepted new connection from {clientAddress[0]}:{clientAddress[1]}")
            # Agrego el socket del cliente a la lista de sockets para manejarlos con select
            socketsList.append(clientSocket)
        else:
            # Si el cliente ya tiene una conexión y algo es recibido
            print("Checking which part of the protocol to execute...")
            message = receiveMessage(notifiedSocket)

            # Saber que responder dependiendo del protocolo
            if message['message'] == "HELLO":
                print("Entering HELLO case...")
                #handshake(clientSocket)  # Hago el handshake con el cliente recién recibido
                msg = "HELLO BACK"
                message = createMessage(msg)

                notifiedSocket.sendall(message)
            elif message['message'] == "PREPARED":
                print("Entering PREPARED case...")
                # Si el cliente está listo para escoger archivo, entonces listarselos
                msg = f"ARCHIVOS: 1. {FILE_1}"
                message = createMessage(msg)

                notifiedSocket.sendall(message)
            # Si el cliente escoge el primer archivo
            elif message['message'] == "1":
                # Abrir el archivo a enviar
                file = open(FILE_1, 'rb')
                # Empezar transmision del archivo
                # Chequear como manejar integridad
                print("Enviando archivo...")
                b = file.read(1024)
                while b:
                    print("Enviando archivo...")
                    notifiedSocket.send(b)
                    b = file.read(1024)
                print("Archivo enviado al cliente exitosamente.")
                #Cierro conexión con el cliente y lo remuevo de la lista de sockets
                notifiedSocket.close()
                socketsList.remove(notifiedSocket)

    for notifiedSocket in exceptionSockets:
        print("Excepcion con un socket.")
        socketsList.remove(notifiedSocket)



'''
clientSocket, addr = serverSocket.accept()
print(f"Connection from {addr} has been established!")

file = open("./files/prueba.pdf", 'rb')

b = file.read(1024)
while b:
    clientSocket.send(b)
    b = file.read(1024)


clientSocket.close()
#clientSocket.send(message)


'''

'''
def handshake(clientSocket):
    try:
        # Ahorita agregamos header
        message = clientSocket.recv(1024)
        while message:
            message = clientSocket.recv(1024)
        #message = message.decode("utf-8")
        print(f"Message handshake received from client: {message}")
        print(message)
        if message.upper() == "HELLO":
            #Si el mensaje es 'hello'. responder con 'hello back'
            message = "HELLO BACK"
            clientSocket.sendall(message.encode("utf-8"))
    except Exception as e:
        print('General error', str(e))
'''