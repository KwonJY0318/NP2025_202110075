# client_basic.py
import socket
import threading

def recv_loop(sock: socket.socket):
    while True:
        try:
            data = sock.recv(1024)
        except OSError:
            break
        if not data:
            break
        print(data.decode("utf-8").rstrip())
    print("[SYSTEM] 서버와의 연결이 종료되었습니다.")


def main():
    host = input("Server IP (예: 127.0.0.1): ").strip()
    port = int(input("Port (예: 5001): ").strip())

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("[SYSTEM] 서버에 연결되었습니다. (/quit 입력 시 종료)")
        t = threading.Thread(target=recv_loop, args=(s,), daemon=True)
        t.start()

        while True:
            msg = input()
            if not msg:
                continue
            s.sendall(msg.encode("utf-8"))
            if msg == "/quit":
                break


if __name__ == "__main__":
    main()
