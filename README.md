# Packet Courier: the TCP vs UDP game

An interactive game that teaches when to use TCP and when to use UDP. Each round gives you a real-world job
(bank transfer, voice call, shooter, video stream...). You choose a protocol, then both protocols race
across a lossy network so you can see why one fits and the other does not.

**Live demo:** https://himeltasinislam.github.io/packet-courier/

## How TCP and UDP are demonstrated
- `index.html` simulates both protocols step by step: TCP handshake, ACKs, retransmission timeouts, slow start,
  in-order delivery (head-of-line blocking), versus UDP fire-and-forget with loss and jitter.
- `server.py` / `client.py` are a real backend using Python `socket` (`SOCK_STREAM` for TCP, `SOCK_DGRAM` for UDP).

Run the real backend:
```
python server.py --loss 0.15      # terminal 1
python client.py                  # terminal 2
```

## Agentic AI in development
Built with Claude as a development partner: it planned the design, generated the simulation engine and the socket
code, and I reviewed, tested and adjusted the parameters. (Add your own notes here: prompts you used, bugs you hit, what you changed.)
