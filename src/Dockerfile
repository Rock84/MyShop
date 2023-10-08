FROM python:3.11.6-alpine3.18

WORKDIR /src

COPY . /src

RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

# указывает что не нужно создаваь кэш файлы с байт кодом
ENV PYTHONDONTWRITEBYTECODE 1
# указывает что нет необходимости кэшировать ввод/вывод
ENV PYTHONUNBUFFERED 1

EXPOSE 8000
