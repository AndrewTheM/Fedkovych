FROM python:3.12.6-alpine

RUN apk add ffmpeg

WORKDIR /usr/src/music-bot

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]