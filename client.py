from socket import *
import sys
from time import sleep
from time import time

bufferSize = 1024

porta = 8080

separationCarac = '<@>'

bytesAdressPair = (('191.187.142.61', porta))

# Inicializando valores
finalDownload = 0
perdaDownload = 0
totalDownload = 0
vazaoDownload = 0
uploadStart = 0
tamanhoEmBytesDownload = 0

s = socket(AF_INET, SOCK_DGRAM)

s.bind(('192.168.15.3', porta))

def receberDoServidor():
    global s
    global bytesAdressPair
    global finalDownload
    global perdaDownload
    global totalDownload
    global vazaoDownload
    global tamanhoEmBytesDownload

    #criando o arquivo que vai receber os dados
    path = 'entrada.txt'
    
    downloadStart = time()
    data = s.recv(bufferSize)
    contador = 0
    with open(path, 'wb') as f:
        
        # enquanto tiver dados para chegar, vai receber e escrever
        while data:
            contador += 1 
            f.write(data)
            print(contador)
            data = s.recv(bufferSize)
            tamanhoEmBytesDownload  += sys.getsizeof(data)
            
            # identifica se o pacote acabou
            if b'<fim>' in data:
                break
    # fim do download
    finalDownload = time()
    perdaDownload = tamanhoEmBytesDownload / 52428800  
    # tempo total
    totalDownload = finalDownload - downloadStart
    vazaoDownload = tamanhoEmBytesDownload / totalDownload
    f.close()
    return


def enviarParaServidor():
    global s
    global bytesAdressPair
    global separationCarac
    global uploadStart

    # Contador que começa em 0
    ack = 0
    
    path = "test.txt"

    #contador em bytes
    tamanhoEmBytes = 0


    with open(path, "rb") as f:

        # Pegar o inicio do upload
        uploadStart = time()

        # envia enquanto não chegar em 50MB
        while tamanhoEmBytes < 52428800:
          
          ack += 1
          # -3 é por conta do separador
          bytesEnviados = f.read(bufferSize-len(str(ack)) - 3)

          stringByte = str(ack) + separationCarac + bytesEnviados.decode('utf-8')

          byteString = bytes(stringByte, 'utf-8')
          tamanhoEmBytes += sys.getsizeof(byteString)  

          print(tamanhoEmBytes)

          s.sendto(byteString, bytesAdressPair)
      
        sleep(1)
        s.sendto(bytes('<fim>', 'utf-8'), bytesAdressPair)
        

    f.close()


    return


enviarParaServidor()
print("Terminou de enviar -> Começou a receber")
sleep(1)
receberDoServidor()

# Esperar um tempo
sleep(3)

# -----------------------------------------------------------------------------------------------------------------
# CONEXAO TCP

porta = 8080
s = socket(AF_INET, SOCK_STREAM)

s.bind(('192.168.15.3', porta))

s.connect(('191.187.142.61', porta))

# Enviar dados de download que servirao para os dados de upload
# Tempo final de download + taxa de perda Download + tamanho em bytes que foi recebido pelo envio
msg = f'{finalDownload} {perdaDownload} {tamanhoEmBytesDownload}'

s.sendall(bytes(msg, 'utf-8'))
                                                              
data = s.recv(1024)

data = data.decode('utf-8')

finalUpload, perdaUpload, tamanhoEmBytesUpload = data.split()

finalUpload = float(finalUpload)
perdaUpload = float(perdaUpload)
tamanhoEmBytesUpload = int(tamanhoEmBytesUpload)

totalUpload = finalUpload - uploadStart

# A vazao precisa ser o tempo que o ultimo byte chega sobre o tempo total de upload
vazaoUpload = tamanhoEmBytesUpload / totalUpload

s.close()

# Depois de finalizada, printar as informaçoes

print('\n---------- DADOS DA CONEXAO ----------\n')
print(f'Tempo total de Download: {(totalDownload):.3f} segundos')
print(f'Taxa de Perda no Download: {(100 - (perdaDownload * 100)):.2f}%')
print(f'Vazao total de Download: {(vazaoDownload):.2f} bytes por segundo')
print(f'Tempo total de Upload: {(totalUpload):.3f}')
print(f'Taxa de Perda no Upload: {(100 - (perdaUpload * 100)):.2f}%')
print(f'Vazao total de Upload: {(vazaoUpload):.2f} bytes por segundo')
