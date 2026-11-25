"""Real TCP + UDP echo server on port 9000 (same port number, two different protocols).
TCP: connection-oriented, reliable. The OS retransmits lost segments, so nothing is lost.
UDP: connectionless. To mimic a bad network we drop datagrams randomly (--loss)."""
import argparse, random, socket, threading

def handle_tcp(conn, addr):
    with conn, conn.makefile("rwb") as f:
        for line in f:           # one message per line
            f.write(line); f.flush()   # echo = application-level ACK

def tcp_server(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port)); s.listen()
    print(f"[TCP] listening on {port}")
    while True:
        conn, addr = s.accept()
        print(f"[TCP] connection from {addr}")
        threading.Thread(target=handle_tcp, args=(conn, addr), daemon=True).start()

def udp_server(host, port, loss):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    print(f"[UDP] listening on {port} (simulated loss {loss:.0%})")
    while True:
        data, addr = s.recvfrom(1024)
        if random.random() < loss:
            continue             # "network" dropped it, nobody will resend
        s.sendto(data, addr)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="0.0.0.0"); ap.add_argument("--port", type=int, default=9000)
    ap.add_argument("--loss", type=float, default=0.15)
    a = ap.parse_args()
    threading.Thread(target=tcp_server, args=(a.host, a.port), daemon=True).start()
    udp_server(a.host, a.port, a.loss)
