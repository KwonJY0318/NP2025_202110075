# chat_server_oo.py
import socket
import threading


class ChatServer:
    def __init__(self, host="0.0.0.0", port=5001):
        self.host = host
        self.port = port
        self.server_sock = None
        self.clients = []          # (conn, addr) 리스트
        self.lock = threading.Lock()

    def start(self):
        """서버 소켓 생성 + accept 루프 시작"""
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen()
        print(f"[SERVER] Listening on {self.host}:{self.port}")

        while True:
            conn, addr = self.server_sock.accept()
            with self.lock:
                self.clients.append((conn, addr))
            print(f"[+] Connected: {addr}")
            self.broadcast(f"[SYSTEM] {addr} 입장")

            th = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
            th.start()

    def broadcast(self, message: str):
        """모든 클라이언트에게 메시지 전송"""
        data = (message + "\n").encode("utf-8")
        with self.lock:
            for conn, _ in list(self.clients):
                try:
                    conn.sendall(data)
                except OSError:
                    # 이미 끊긴 소켓일 수 있음
                    pass

    def handle_client(self, conn: socket.socket, addr):
        """각 클라이언트를 담당하는 쓰레드 함수"""
        with conn:
            try:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    msg = data.decode("utf-8").strip()
                    if msg == "/quit":
                        break
                    self.broadcast(f"[{addr}] {msg}")
            finally:
                # 접속 종료 처리
                with self.lock:
                    for c, a in list(self.clients):
                        if c is conn:
                            self.clients.remove((c, a))
                            break
                self.broadcast(f"[SYSTEM] {addr} 퇴장")
                print(f"[-] Disconnected: {addr}")


if __name__ == "__main__":
    server = ChatServer(host="0.0.0.0", port=5001)
    server.start()
