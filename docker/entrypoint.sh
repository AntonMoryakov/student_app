#!/bin/sh
set -e

echo "Ожидание готовности базы данных..."

python -c "
import os
import socket
import time
import sys

host = os.getenv('DB_HOST', 'db')
port = int(os.getenv('DB_PORT', '5432'))

for attempt in range(30):
    try:
        with socket.create_connection((host, port), timeout=2):
            print('База данных доступна')
            sys.exit(0)
    except OSError:
        print(f'Попытка {attempt + 1}/30: база данных еще недоступна')
        time.sleep(2)

print('Не удалось дождаться готовности базы данных')
sys.exit(1)
"

echo "Запуск приложения..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000