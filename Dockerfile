FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Установка зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev curl wget gnupg unzip \
    chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Символическая ссылка для chromedriver
RUN ln -s /usr/bin/chromedriver /usr/local/bin/chromedriver

# requirements.txt
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем проект
COPY . .

# EntryPoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

CMD ["/app/entrypoint.sh"]
