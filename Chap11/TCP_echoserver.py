from socket import *
import threading
import sys

port = 2500
BUFSIZE = 1024

# 1. 클라이언트 통신을 담당할 함수 (스레드에서 실행)
def handler(c_sock, addr):
    # 연결된 클라이언트 정보 출력
    print(f'새로운 클라이언트 연결됨: {addr[0]}:{addr[1]}')
    
    while True:
        try:
            # 데이터 수신
            data = c_sock.recv(BUFSIZE)
            
            # 클라이언트가 정상적으로 연결을 닫은 경우 (데이터가 비어있음)
            if not data:
                print(f'{addr[0]}:{addr[1]} 연결 종료 (정상)')
                break
                
        except ConnectionResetError: # 클라이언트가 강제 종료했을 때의 예외 처리
            print(f'{addr[0]}:{addr[1]} 연결 종료 (비정상/강제 종료)')
            break
        except Exception as e:
            print(f"오류 발생: {e}")
            break
        
        # 수신한 데이터 출력 및 에코 (송신)
        print(f"[{addr[0]}:{addr[1]}] 수신 데이터: {data.decode()}")
        
        try:
            c_sock.sendall(data) # sendall 사용 권장 (모든 데이터 전송 보장)
        except:
            break

    c_sock.close() # 통신이 끝나면 소켓을 닫고 스레드 종료

# 2. 메인 서버 로직
def main():
    sock = socket(AF_INET, SOCK_STREAM)
    try:
        # 이미 사용 중인 포트를 재사용할 수 있도록 설정 (선택 사항)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind(('', port))
    except Exception as e:
        print(f"바인딩 오류 발생: {e}")
        sys.exit() # 프로그램 종료

    sock.listen(5)
    print("--------------------------------------")
    print(f"TCP 멀티쓰레드 에코 서버 시작 (Port: {port})")
    print("클라이언트 연결을 기다리는 중...")
    
    # 무한 루프: 항상 새로운 클라이언트 연결을 수락
    while True:
        try:
            # 블로킹: 새로운 연결이 들어올 때까지 대기
            c_sock, addr = sock.accept()
            
            # 연결 수락 시: 통신을 전담할 스레드 생성 및 시작
            t = threading.Thread(target=handler, args=(c_sock, addr))
            t.daemon = True # 메인 프로그램 종료 시 스레드도 자동 종료
            t.start()
            
        except KeyboardInterrupt:
            # Ctrl+C 입력 시 서버 종료
            print("\n서버 종료 중...")
            break
        except Exception as e:
            print(f"메인 루프 오류: {e}")
            continue

    sock.close()

if __name__ == '__main__':
    main()