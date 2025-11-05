class TCPServer:
    def __init__(self, port): # 소켓을 생성하고 바인드 후 연결 대기
        import socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("", port))
        self.sock.listen(5)
    
    def Accept(self): # 연결을 허용하고 클라이언트 소켓과 주소 반환
        self.c_sock, self.c_addr = self.sock.accept()
        return self.c_sock, self.c_addr

if __name__ == '__main__':
    sock = TCPServer(2500) # 소켓 생성과 연결
    c, addr = sock.Accept()
    print('수신 메시지:', c.recv(1024).decode())
    msg = "Hello Client"
    c.send(msg.encode())
    c.close()