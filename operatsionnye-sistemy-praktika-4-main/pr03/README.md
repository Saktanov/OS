# ПР-3. Процессы в Linux

## Цель

Изучить процессы, состояния, `fork`, `exec`, `wait`, зомби, сирот и `/proc`.

## Запуск

```bash
ps -eo pid,ppid,stat,cmd --forest | head -40
sleep 300 &
cat /proc/<PID>/status
kill <PID>

python3 fork_demo.py
python3 ptree.py
python3 runner.py 3 /bin/echo hello
python3 zombie_demo.py
python3 orphan_demo.py
python3 cow_memory.py
```

## Выводы

- `fork()` создаёт почти копию процесса и возвращает разные значения родителю и ребёнку.
- `exec()` заменяет образ процесса новой программой.
- `wait()` нужен, чтобы родитель забрал код завершения ребёнка и не оставил зомби.
- Сирота после завершения родителя усыновляется `init`/`systemd` или subreaper.
- Copy-on-write означает, что память после `fork` физически копируется только при записи.
