# Install

Клонирование репозитория и смена директории:
```
git clone https://github.com/fedoxyz/NutritionTGBot
cd NutritionTGBot
```

## Docker Install
Для запуска бота через Docker:
Запуск Docker контейнеров на локальной машине.

1. Установить `docker` и `docker compose`

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

Для использования environment переменных:
```
mv demo.env .env
```

.env должен содержать URL базы данных и токен Telegram бота

Build контейнеров и запуск контейнеров
```
docker compose up --build
```
Для запуска в фоновом режиме использовать флаг `-d`
```
docker compose up --build -d
```
