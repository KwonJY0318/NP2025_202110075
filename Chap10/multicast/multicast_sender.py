import socket
import struct

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5000

# UDP 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# TTL(Time To Live) 설정: 1이면 로컬 네트워크까지만 전파
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

print(f"Multicast sender to group {MCAST_GRP}:{MCAST_PORT}")

while True:
    msg = input("Multicast Message: ")
    sock.sendto(msg.encode(), (MCAST_GRP, MCAST_PORT))
