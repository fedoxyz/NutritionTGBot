# Install

Клонирование репозитория и смена директории:
```
git clone https://github.com/fedoxyz/NutritionTGBot
cd NutritionTGBot
```

## venv

Создать виртуальную среду:
```
virtualenv venv
```

Активировать виртуальную среду:
Linux:
```
source venv/bin/activate
```

Установить необходимые библиотеки
```
pip install -r requirements.txt
```

Для использования environment переменных:
```
mv demo.env .env
```

.env должен содержать URL базы данных и токен Telegram бота

Запуск телеграм бота:
Linux:
```
python3 bot.py
```


## Docker Install
Для запуска бота через Docker:
Запуск Docker контейнеров на локальной машине.

1. Установить Docker
2. Запустить

Для ollama контейнера установите `nvidia-container-toolkit`

Linux Ubuntu
```
sudo apt-get install -y nvidia-container-toolkit
```

Конфигурация для использования Nvidia в контейнере 
```
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

Build контейнеров и запуск контейнеров
```
docker compose up --build
```
Для запуска в фоновом режиме использовать флаг `-d`
```
docker compose up --build -d
```

При успешном запуске всех контейнеров:
```
[+] Running 4/4
 ✔ Network nutritiontgbot_default  Created                  xxx.3s
 ✔ Container postgres-container    Started                  xxx.6s
 ✔ Container ollama-container      Started                  xxx.6s
 ✔ Container bot-container         Started                  xxx.6s
```
