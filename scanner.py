import socket
import threading

target = "192.168.1.129"
open_ports = []
lock = threading.Lock()
semaphore = threading.Semaphore(100)

def scan_port(port):
	with semaphore:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(0.5)
		result = sock.connect_ex((target, port))
		if result == 0:
			with lock:
				open_ports.append(port)
				print(f"Port {port} is open")
		sock.close()

threads = []
for port in range(5000, 8080):
	t = threading.Thread(target=scan_port, args=(port,))
	threads.append(t)
	t.start()

for t in threads:
	t.join()

print(f"\nOpen ports: {sorted(open_ports)}")
