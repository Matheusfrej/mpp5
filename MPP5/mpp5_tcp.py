from socket import *

s = socket(AF_INET, SOCK_STREAM)
s.bind(('192.168.0.3', 8080))
s.listen(1)

while True:
  conn, addr = s.accept()

  print(f"Servidor conectado com: {addr[0]} {addr[1]}")

  while True:
    data = conn.recv(1024)
    data = str(repr(data))[2:-1]
    print(data)
    
    conn.sendall(bytes(data, 'utf-8'))

  conn.close()