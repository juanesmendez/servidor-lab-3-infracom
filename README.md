# TCP File Transfer Server 📂🗄🗃

## Description

TCP server implemented in Python 🐍 that hosts files for a client to download them. The client can be found in the following repository: https://github.com/juanesmendez/tcp-client. The integrity of the files received by the client is guaranteed using a hash digest, which is calculated by the server and then sent to the client for him to compare it against the one he calculates on the byte stream he receives.

### Python libraries 📚
The following python libraries and classes were used in the client application:

- `socket`
- `pickle` 🥒: For transferring the file in byte chunks.
- `hashlib` 🔑#️⃣: For calculating the hash digest of the file that is transferred to the client.
- `select`: For handling multiple users at once.

## How to run the project?

The files available for the client to download are located in the `/files` directory. Please follow the steps below to run the project successfully:

1. Install `Python 3.7`.
2. Run `python3.7 server.py`
    - Your server will now be listening to TCP connections in the `port` 1236.
    
NOTE: You can change the port number in line #8 in the `client.py` file, but please keep in mind that you will have to change the port number as well in the `client` application in order to establish a connection with the `server`.
