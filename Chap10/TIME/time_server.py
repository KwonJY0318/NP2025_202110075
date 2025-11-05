# time_server.py

import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 주소 변경: 'localhost' 대신 명시적인 루프백 IP '127.0.0.1' 사용
address = ('192.168.214.161', 5000)
s.bind(address)
s.listen(5)

print(f"✅ Time Server started on {address}. Waiting for connections...")
# 

while True:
    try:
        client, addr = s.accept()
        print(f"Connection requested from {addr}")
        
        # 현재 시간을 문자열로 포맷하여 클라이언트에게 전송
        current_time = time.ctime(time.time())
        client.send(current_time.encode('utf-8'))
        
        print(f"Sent time: {current_time}")
        client.close()
    except Exception as e:
        print(f"An error occurred: {e}")
        # 서버 오류가 발생하더라도 루프는 계속 실행되도록 유지