# broadcast_server.py
from socket import *

sock = socket(AF_INET, SOCK_DGRAM)     # UDP 소켓
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 주소 재사용
sock.bind(("", 10000))                 # 모든 IP에서 포트 10000으로 들어오는 패킷 수신

while True:
    msg, addr = sock.recvfrom(1024)    # 메시지 수신
    print(msg.decode())
