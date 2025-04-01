# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Prevents Python from writing .pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app/schoolmind

# Install system dependencies (если нужны, например, gcc, libpq-dev для psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/schoolmind/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project code
COPY . /app/

# Скопирует entrypoint.sh в контейнер и сделайте его исполняемым
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose port 8000 (Django)
EXPOSE 8000

# Используем entrypoint.sh как точку входа
CMD ["/app/entrypoint.sh"]

# Command to run the Django application via Gunicorn
#CMD ["gunicorn", "schoolmind.wsgi:application", "--bind", "0.0.0.0:8000"]
