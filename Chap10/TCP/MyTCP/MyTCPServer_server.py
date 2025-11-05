import MyTCPServer as mt
import sys
port = 2500

if len(sys.argv)>1: #명령 실행시 포트를 지정하면 지정 포트 사용
    port = int(eval(sys.argv[1]))

sock = mt.TCPServer(port)
c, addr = sock.Accept() # 소켓과 address 반환

while True:
    print('Connected by ', addr[0], addr[1]) # 주소와 포트
    data = c.recv(1024)
    if not data:
        break
    print('Received message:', data.decode())
    c.send(data)

c.close()