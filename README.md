
Поднимаем базу данных
```
docker compose up -d
```

Устанавливаем python-зависимости
```
poetry install
```

В файле ***test_audio.ipynb*** представлен пример работы
1. Записываем аудио из файла raw/horse.mp3 в базу данных в bucket='bucket_in'
2. В базе данных находиться задача (task), которая увеличивает громкость данных из bucket='bucket_in' и кладет их в bucket='bucket_out'
3. Далее мы читаем данные из bucket='bucket_out' и преобразуем обратно в аудио raw/horse_out.mp3