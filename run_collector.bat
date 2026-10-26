@echo off
cd /d "%~dp0"
"C:\Users\rifqi\AppData\Local\Programs\Python\Python312\python.exe" scripts\daily_news_collector.py >> scripts\collector_log.txt 2>&1
