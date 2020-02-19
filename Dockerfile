# Используем базовый образ
FROM python:slim

# Создаём директорию бота
RUN mkdir /enzymes_bot

# Копируем все файлы из текущей директории в директорию бота
COPY . /enzymes_bot

# Устанавливаем рабочую директорию
WORKDIR /enzymes_bot

# Устанавливаем pytelegrambotapi
RUN pip3 install --no-cache-dir pytelegrambotapi

# Указываем команды для выполнения после запуска контейнера
CMD ["python3", "bot.py"]
