#
# SimpleEchoTCPServer.py
#

import socket

HOST = '127.0.0.1'
serverPort = 9999
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, serverPort))
serverSocket.listen(1)

print("The server is ready to receive message on port", serverPort)

while True:
    (connectionSocket, clientAddress) = serverSocket.accept()
    message = connectionSocket.recv(2048)
    print('Recived from',clientAddress, message.decode())
    connectionSocket.close()
serverSocket.close