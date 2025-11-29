# chat_client_oo.py
import socket
import threading


class ChatClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sock: socket.socket | None = None

    def connect(self):
        """서버에 연결하고, recv 쓰레드 + send 루프 시작"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        print("[SYSTEM] 서버에 연결되었습니다. (/quit 입력 시 종료)")

        recv_thread = threading.Thread(target=self.recv_loop, daemon=True)
        recv_thread.start()

        self.send_loop()

    def recv_loop(self):
        """서버로부터 오는 메시지 출력"""
        assert self.sock is not None
        while True:
            try:
                data = self.sock.recv(1024)
            except OSError:
                break
            if not data:
                break
            print(data.decode("utf-8").rstrip())
        print("[SYSTEM] 서버 연결 종료")
        try:
            self.sock.close()
        except OSError:
            pass

    def send_loop(self):
        """키보드 입력을 서버로 전송"""
        assert self.sock is not None
        while True:
            msg = input()
            if not msg:
                continue
            try:
                self.sock.sendall(msg.encode("utf-8"))
            except OSError:
                break
            if msg == "/quit":
                break
        try:
            self.sock.close()
        except OSError:
            pass


if __name__ == "__main__":
    host = input("Server IP (예: 192.168.219.xxx): ").strip()
    port = int(input("Port (예: 5001): ").strip())
    client = ChatClient(host, port)
    client.connect()
