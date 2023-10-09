FROM python:3.11.6-alpine3.18

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# указывает что не нужно создаваь кэш файлы с байт кодом
ENV PYTHONDONTWRITEBYTECODE 1
# указывает что нет необходимости кэшировать ввод/вывод
ENV PYTHONUNBUFFERED 1

EXPOSE 8000
