# Базовый образ Python
FROM python:3.12.9

# Рабочая директория в контейнере
WORKDIR /app

# Копируем зависимости
COPY packages.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r packages.txt

# Копируем остальные файлы
COPY . .

# Запускаем бота
CMD ["python", "main.py"]
CMD ["python", "parser.py"]