# TCPClient_easy.py
import socket

# TCP 소켓 생성
sock = socket.create_connection(('192.168.214.161', 2500)) # 소켓 생성과 연결

# 데이터 전송
message = "Client Message"
print('sending {}'.format(message))
sock.sendall(message.encode()) # 데이터를 모두 전송

data = sock.recv(1024) # 데이터 수신
print('received {}'.format(data.decode()))
print('closing socket')
sock.close()