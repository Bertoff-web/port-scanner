import socket
import threading
import json
import os
from datetime import datetime
import config

open_ports = []
lock = threading.Lock()


SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 3306: "MySQL", 5432: "PostgreSQL",
    6379: "Redis", 8080: "HTTP-alt", 27017: "MongoDB"
}

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(config.TIMEOUT)
        result = sock.connect_ex((target, port))
        sock.close()

        if result == 0:
            service = SERVICES.get(port, "Desconhecido")
            with lock:
                open_ports.append({"port": port, "service": service})
            print(f"  [+] Porta {port:5d} ABERTA  → {service}")
    except Exception:
        pass

def run_scan(target=None, start=None, end=None):
    target = target or config.TARGET
    start  = start  or config.START_PORT
    end    = end    or config.END_PORT

    print(f"\n[*] Iniciando scan em {target}")
    print(f"[*] Portas: {start} → {end}")
    print(f"[*] Threads: {config.MAX_THREADS}\n")

    threads = []
    semaphore = threading.Semaphore(config.MAX_THREADS)

    def worker(port):
        with semaphore:
            scan_port(target, port)

    for port in range(start, end + 1):
        t = threading.Thread(target=worker, args=(port,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return sorted(open_ports, key=lambda x: x["port"])

if __name__ == "__main__":
    start_time = datetime.now()
    results = run_scan()
    duration = (datetime.now() - start_time).seconds

    print(f"\n[*] Scan concluído em {duration}s")
    print(f"[*] {len(results)} porta(s) aberta(s) encontrada(s)\n")

    
    os.makedirs("reports", exist_ok=True)
    report = {
        "target": config.TARGET,
        "timestamp": datetime.now().isoformat(),
        "duration_seconds": duration,
        "open_ports": results
    }
    with open(config.REPORT_FILE, "w") as f:
        json.dump(report, f, indent=2)

    print(f"[*] Relatório salvo em: {config.REPORT_FILE}")