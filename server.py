import socket
import select
import pickle
import hashlib

HEADERSIZE = 10
IP = "0.0.0.0"
PORT = 1236
FILE_1 = "./files/prueba.pdf"
FILE_2 = "./files/video-5.mp4"

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


def receiveMessageText(clientSocket):
    print("Receiving message from client...")
    try:
        # Desarmar header para saber el tamaño en bytes del mensaje
        text = clientSocket.recv(1024)
        text = text.decode("utf-8").strip()
        print(f"Message received from client: {text}")
        print(text)
        return text
    except Exception as e:
        print('General error', str(e))



def sendFile(fileName):
    file = open(fileName, 'rb')
    data = file.read()
    file.close()
    print("File size:", len(data))
    messageHeader = f"{len(data):<{HEADERSIZE}}".encode("utf-8")
    print(f"Message header: {messageHeader}")
    #print(f"Message payload: {data}")

    # Retornamos el header con el mensaje convertido en bytes
    #print(f"Sending message '{messageHeader + data}'")
    return messageHeader + data




def sendDigest(fileName):
    print("Iniciando envio del digest del archivo...")
    file = open(fileName, 'rb')
    data = file.read()
    file.close()

    m = hashlib.sha256()
    m.update(data)
    digest = m.digest()

    messageHeader = f"{len(digest):<{HEADERSIZE}}".encode("utf-8")
    print(f"Message header: {messageHeader}")
    print(f"Sending digest '{messageHeader + digest}'")
    #digest = createMessage(m.digest())  # Creamos un mensaje con el digest del archivo
    #notifiedSocket.sendall(digest)
    return messageHeader + digest

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serverSocket.bind((IP, PORT))
serverSocket.listen(25) # Listen to five connections

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
            #message = receiveMessageText(notifiedSocket)

            # Saber que responder dependiendo del protocolo
            if message == "TEST":
                print("Entering TEST case...")
                notifiedSocket.sendall("OK".encode("utf-8"))
                notifiedSocket.close()
                socketsList.remove(notifiedSocket)
            elif message['message'] == "HELLO":
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
                file = sendFile(FILE_1)
                notifiedSocket.sendall(file)

            elif message['message'] == "2":
                file = sendFile(FILE_2)
                notifiedSocket.sendall(file)

            elif message['message'] == "DIGEST1":
                #Enviar el digest del archivo al cliente:
                digest = sendDigest(FILE_1)
                notifiedSocket.sendall(digest)

                #Cierro conexión con el cliente y lo remuevo de la lista de sockets

                notifiedSocket.close()
                socketsList.remove(notifiedSocket)
            elif message['message'] == "DIGEST2":
                # Enviar el digest del archivo al cliente:
                digest = sendDigest(FILE_2)
                notifiedSocket.sendall(digest)

                # Cierro conexión con el cliente y lo remuevo de la lista de sockets

                notifiedSocket.close()
                socketsList.remove(notifiedSocket)

            elif message['message'] == "TEST":
                message = createMessage("OK")
                notifiedSocket.sendall(message)
                notifiedSocket.close()
                socketsList.remove(notifiedSocket)


    for notifiedSocket in exceptionSockets:
        print("Excepcion con un socket.")
        socketsList.remove(notifiedSocket)


'''
def sendFile(fileName):
    print("Iniciando envio del archivo...")
    file = open(fileName, 'rb')
    data = file.read()
    file.close()
    # Chequear el atributo message size, puede que esté incorrecto
    msg = {"fileSize": len(data),
           "file": data}
    msg = pickle.dumps(msg)
    # Añadir header de 10 bytes
    messageHeader = f"{len(msg):<{HEADERSIZE}}".encode("utf-8")

    print(f"Message header: {messageHeader}")
    #print(f"Message payload: {msg}")

    # Retornamos el header con el mensaje convertido en bytes
    #print(f"Sending message '{messageHeader + msg}'")
    print("Archivo enviado exitosamente.")
    return messageHeader + msg
'''

'''
                # Abrir el archivo a enviar
                file = open(FILE_1, 'rb')
                # Empezar transmision del archivo
                # Chequear como manejar integridad
                print("Enviando archivo...")
                b = file.read(1024)
                i=0
                while b:
                    print(f"Enviando archivo parte {i}...")
                    notifiedSocket.send(b)
                    b = file.read(1024)
                    i=i+1
                print("Archivo enviado al cliente exitosamente.")
                file.close()

'''




