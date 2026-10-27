# ПР-7. Межпроцессное взаимодействие

## Цель

Организовать IPC через pipe, FIFO, сигналы, subprocess, Unix socket и shared memory.

## Запуск

```bash
python3 pipe_demo.py
python3 subprocess_pipe.py
python3 signal_demo.py
```

FIFO:

```bash
mkfifo /tmp/chan
cat /tmp/chan
echo hello > /tmp/chan
rm /tmp/chan
```

Клиент-сервер FIFO:

```bash
python3 fifo_server.py
python3 fifo_client.py "10 * 5"
python3 fifo_client.py quit
```

Unix socket:

```bash
python3 unix_socket_server.py
python3 unix_socket_client.py "3 + 7"
python3 unix_socket_client.py quit
```

Shared memory:

```bash
python3 shared_memory_demo.py
```

## Вывод

FIFO блокируется, если одна сторона ещё не открыла канал. Shared memory быстрее для больших данных, потому что избегает лишнего копирования, но требует синхронизации.
