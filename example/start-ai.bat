@echo off
start venv\Scripts\python main.py bot1.json
ping 127.0.0.1 -n 1 > nul
start venv\Scripts\python main.py bot2.json
exit
rem -----------------------------------------
ping 127.0.0.1 -n 1 > nul
start venv\Scripts\python main.py bot3.json
ping 127.0.0.1 -n 1 > nul
start venv\Scripts\python main.py bot4.json
ping 127.0.0.1 -n 1 > nul
start venv\Scripts\python main.py bot5.json
ping 127.0.0.1 -n 1 > nul
start venv\Scripts\python main.py bot6.json
