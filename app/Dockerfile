FROM python:3.12.6

# Указываем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
#CMD ["python", "main.py"]

# Устанавливаем supervisor
RUN apt-get update && \
    apt-get install -y supervisor

# Конфигурация supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Команда для запуска supervisor
CMD ["/usr/bin/supervisord"]