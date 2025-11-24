import socket
import struct

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5000
BUFFSIZE = 1024

# UDP 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 모든 인터페이스에서 MCAST_PORT 수신
sock.bind(('', MCAST_PORT))

# 멀티캐스트 그룹 가입
mreq = struct.pack(
    "4sl",
    socket.inet_aton(MCAST_GRP),
    socket.INADDR_ANY
)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print(f"Multicast receiver joined group {MCAST_GRP}:{MCAST_PORT}")

while True:
    data, addr = sock.recvfrom(BUFFSIZE)
    print(f"Received from {addr}: {data.decode()}")
