# time_client.py

import socket

# 주소 변경: 'localhost' 대신 명시적인 루프백 IP '127.0.0.1' 사용
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ("172.21.101.22", 5000)

try:
    print(f"Attempting to connect to {address}...")
    sock.connect((address))
    
    # 서버로부터 데이터를 수신하고 디코딩
    received_data = sock.recv(1024).decode('utf-8')
    print("현재 시각: ", received_data)
    
except ConnectionRefusedError:
    print("\n❌ ConnectionRefusedError: 서버가 해당 주소/포트에서 실행 중인지 확인하세요.")
except Exception as e:
    print(f"\nAn error occurred: {e}")
finally:
    # 연결이 성공했든 실패했든 소켓을 닫습니다.
    sock.close()