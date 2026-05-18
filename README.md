# 🔍 Scanner de Portas

Scanner de portas em Python com threading para verificar quais serviços estão ativos em um alvo.

## O que ele faz

- Varre portas 1 a 1024 em paralelo com threading
- Identifica serviços conhecidos (SSH, HTTP, FTP, SMB...)
- Gera relatório em JSON com timestamp e duração

## Como usar

```bash
python scanner.py
python report.py
```

## Exemplo de saída
