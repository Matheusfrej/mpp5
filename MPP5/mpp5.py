import socket
import os

localPort = 8080
bufferSize = 524288

UDPServerSocket=socket.socket(family=socket.AF_INET,type = socket.SOCK_DGRAM)

UDPServerSocket.bind(('192.168.0.3', localPort))

print("listening")

def receberDoCliente():
    return


def enviarParaCliente():
    global UDPServerSocket
    global bytesAdressPair
    # Contador que começa em 0
    ack = 0
    
    path = "test.txt"

    #contador em bytes
    tamanhoEmBytes = 0

    with open(path, "rb") as f:

        bytesEnviados = f.read(bufferSize)
        tamanhoEmBytes += bufferSize

        # envia enquanto não chegar em 50MB
        while tamanhoEmBytes < 52428800:
            ack += 1
            tamanhoEmBytes += bufferSize
            stringAck = bytes(f'Mensagem {ack}: ', 'utf-8')

            #tamanho da mensagem acima
            tamanhoEmBytes += len(str(ack)) + 11
            
            UDPServerSocket.sendto(stringAck, bytesAdressPair[1])
            UDPServerSocket.sendto(bytesEnviados, bytesAdressPair[1])
            # ler os bytes do arquivo
            bytesEnviados = f.read(bufferSize)


    return

while True:

    bytesAdressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAdressPair[0]
    UDPServerSocket.sendto(message, bytesAdressPair[1])
    print(message)