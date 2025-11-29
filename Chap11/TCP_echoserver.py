from socket import *

port = 2500
BUFSIZE = 1024

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(('', port))
sock.listen(5) # 최대 대기 틀라이언트 수
print("클라이언트 기다리는 중...")
c_sock, (r_host, r_port) = sock.accept()
print('connected_by', r_host, r_port)
while True:
    try:
        data = c_sock.recv(BUFSIZE)
        if not data:
            c_sock.close()
            print('연결이 종료되었습니다.')
            break
    except:
        print("연결이 종료되었습니다.")
        c_sock.close() #소켓을 닫는다.
        break # 무한루프 종료
    else:
        print(data.decode())

    try:
        c_sock.send(data)
    except:
        print("연결 종료로 인한 예외 발생")
        c_sock.close()
        break