import socket

port = 2500
BUFFSIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", port))   # 모든 IP에서 오는 메시지 수신

print("UDP chat server started. waiting for client...")

while True:  # 무한 루프
    print("<- ", end="")                    # 상대방 메시지 표시 프롬프트
    data, addr = sock.recvfrom(BUFFSIZE)    # 수신 (데이터, (ip, port))
    print(data.decode())                    # 받은 메시지 출력

    resp = input("-> ")                     # 내가 보낼 메시지 입력
    sock.sendto(resp.encode(), addr)        # 입력한 메시지 전송
