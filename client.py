"""Sends 50 messages over TCP and over UDP to server.py and compares the results."""
import socket, sys, time
host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT, N = 9000, 50

def run_tcp():
    s = socket.create_connection((host, PORT))      # 3-way handshake happens here
    f = s.makefile("rwb"); ok = 0; t = time.time()
    for i in range(N):
        f.write(f"msg {i}\n".encode()); f.flush()
        if f.readline().decode().strip() == f"msg {i}": ok += 1
    return ok, time.time() - t

def run_udp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.settimeout(0.2)
    ok = 0; t = time.time()
    for i in range(N):
        s.sendto(f"msg {i}".encode(), (host, PORT))  # no handshake, no guarantee
        try: s.recvfrom(1024); ok += 1
        except socket.timeout: pass
    return ok, time.time() - t

for name, fn in (("TCP", run_tcp), ("UDP", run_udp)):
    ok, secs = fn()
    print(f"{name}: {ok}/{N} echoed back, {secs:.2f}s")
