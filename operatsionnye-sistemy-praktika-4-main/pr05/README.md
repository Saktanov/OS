# ПР-5. Симулятор планирования CPU

## Цель

Реализовать FCFS, SJF, SRTF, Priority и Round Robin, сравнить метрики.

## Запуск

```bash
python3 sched.py --algo fcfs set1.txt
python3 sched.py --algo sjf set1.txt
python3 sched.py --algo srtf set1.txt
python3 sched.py --algo priority set1.txt
python3 sched.py --algo rr --quantum 3 set1.txt
```

## Проверка set1

Для SRTF и RR результаты совпадают с эталоном из задания:

- SRTF: среднее ожидание `6.5`, средний оборот `13.0`;
- RR q=3: среднее ожидание `13.5`, средний оборот `20.0`.

Для FCFS программа считает по стандартной формуле `waiting = completion - arrival - burst`.
На наборе `P1 0 8`, `P2 1 4`, `P3 2 9`, `P4 3 5` получается:

- FCFS: среднее ожидание `8.75`, средний оборот `15.25`.

## Вывод

SJF/SRTF хорошо уменьшают ожидание для коротких задач, но в реальной ОС точный будущий burst неизвестен. Round Robin лучше подходит для интерактивности, но маленький квант увеличивает число переключений контекста.
