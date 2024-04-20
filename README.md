
Поднимаем базу данных
```
docker-compose up -d
```

Устанавливаем системные зависимости
```
sudo apt-get install libportaudio2
```

Устанавливаем python-зависимости
```
poetry install
```

Запускаем в первой консоли считывание аудио из базы данных
```
poetry run python3 read.py
```

Во второй консоли запускаем запись аудио в базу данных
```
poetry run python3 write.py
```
