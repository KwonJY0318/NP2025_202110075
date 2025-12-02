from socket import *
import argparse

BUFSIZE = 1024

# 1) 명령 인자 설정
parser = argparse.ArgumentParser(description="TCP Dummy Client with -s, -p options")
parser.add_argument('-s', default="192.168.214.161", help="Server IP address")   # 서버 IP
parser.add_argument('-p', type=int, default=2500, help="Port number")      # 포트 번호
args = parser.parse_args()

# 2) 소켓 생성 및 서버 연결
sock = socket(AF_INET, SOCK_STREAM)
sock.connect((args.s, args.p))
print(f"서버에 연결되었습니다: {args.s}:{args.p}")

# 3) 에코 테스트 루프
while True:
    msg = input("보낼 메시지 입력 (quit 입력 시 종료): ")
    if msg == "quit":
        break

    # 서버로 전송
    sock.send(msg.encode())

    # 서버로부터 에코 데이터 수신
    data = sock.recv(BUFSIZE)
    if not data:
        print("서버로부터 데이터 수신 실패(연결 종료)")
        break

    print("서버 응답:", data.decode())

sock.close()
print("클라이언트 종료")
