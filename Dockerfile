FROM python:3.10.12-alpine

WORKDIR /api

COPY . /app

RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt

# указывает что не нужно создаваь кэш файлы с байт кодом
ENV PYTHONDONTWRITEBYTECODE 1
# указывает что нет необходимости кэшировать ввод/вывод
ENV PYTHONUNBUFFERED 1

EXPOSE 8000