```
git clone https://github.com/fedoxyz/NutritionTGBot
cd NutritionTGBot
virtualenv venv
source venv/bin/activate # Linux
pip install -r requirements.txt
```

```
mv demo.env .env
```

```
.env должен содержать URL базы данных и токен Telegram бота
```

```
python3 bot.py # Linux
```



Для локального запуска бота:
можно запустить бота на локальной машине, в Докере.

Для этого нужно:

1. Установить Docker
2. Запустить

```
docker compose up --build -d
```

```
[+] Running 4/4
 ✔ Network nutritiontgbot_default  Created                  xxx.3s
 ✔ Container postgres-container    Started                  xxx.6s
 ✔ Container ollama-container      Started                  xxx.6s
 ✔ Container bot-container         Started                  xxx.6s
```
