FROM python:3.9.0-alpine
WORKDIR /usr/src/app
COPY app/* ./
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "main.py"]