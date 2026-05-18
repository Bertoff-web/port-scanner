import json
import config

with open(config.REPORT_FILE) as f:
    data = json.load(f)

print(f"\n Relatório de Scan")
print(f"Alvo:    {data['target']}")
print(f"Data:    {data['timestamp']}")
print(f"Duração: {data['duration_seconds']}s")
print(f"\n{'Porta':<8} {'Serviço'}")
print("-" * 25)
for entry in data["open_ports"]:
    print(f"{entry['port']:<8} {entry['service']}")