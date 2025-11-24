import socket

SERVER_IP = "192.168.219.163"  # 윈도우 서버 IPv4 주소
port = 2500
BUFFSIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("UDP chat client started. you can chat now.")

while True:
    # 내가 먼저 보내기
    msg = input("-> ")                                   # 보낼 메시지 입력
    sock.sendto(msg.encode(), (SERVER_IP, port))         # 서버로 전송

    # 서버에서 온 메시지 받기
    print("<- ", end="")
    data, addr = sock.recvfrom(BUFFSIZE)
    print(data.decode())
