# broadcast_client.py
from socket import *

addr = ('<broadcast>', 10000)          # 브로드캐스트 주소

sock = socket(AF_INET, SOCK_DGRAM)
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)  # 브로드캐스트 옵션

while True:
    smsg = input("Broadcast Message: ")
    sock.sendto(smsg.encode(), addr)     # 메시지를 네트워크 전체에 전송
