# server_basic.py
import socket
import threading

HOST = "0.0.0.0"   # 모든 인터페이스에서 수신
PORT = 5001

clients = []       # (conn, addr) 튜플 리스트
lock = threading.Lock()


def broadcast(message: str):
    """모든 클라이언트에게 메시지 전송 (송신자 포함)"""
    data = (message + "\n").encode("utf-8")
    with lock:
        for conn, _ in clients:
            try:
                conn.sendall(data)
            except OSError:
                # 이미 끊긴 소켓일 수 있음 → 무시
                pass


def handle_client(conn: socket.socket, addr):
    with conn:
        print(f"[+] Connected: {addr}")
        broadcast(f"[SYSTEM] {addr} 님이 입장했습니다.")

        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                msg = data.decode("utf-8").strip()
                if msg == "/quit":
                    break
                broadcast(f"[{addr}] {msg}")
        finally:
            # 리스트에서 제거
            with lock:
                for c, a in list(clients):
                    if c is conn:
                        clients.remove((c, a))
                        break
            broadcast(f"[SYSTEM] {addr} 님이 퇴장했습니다.")
            print(f"[-] Disconnected: {addr}")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"[SERVER] Listening on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            with lock:
                clients.append((conn, addr))
            th = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            th.start()


if __name__ == "__main__":
    main()
