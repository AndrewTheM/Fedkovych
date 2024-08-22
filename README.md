### Підняти RTMP сервер (Docker контейнер)
```
docker run -it -p 1935:1935 -p 8080:80 --rm alfg/nginx-rtmp
```

### Закинути відео потік через FFmpeg
```
ffmpeg -re -i $VIDEO_PATH -c:v libx264 -c:a aac -ar 44100 -ac 1 -f flv rtmp://localhost:1935/stream/radio
```

- -re specifies that input will be read at its native framerate.
- -i $VIDEO_PATH specifies the path to our input file.
- -c:v is set to copy, meaning that you’re copying over the video format
- -c:a has other parameters, namely aac -ar 44100 -ac 1, because you need to resample the audio to an RTMP-friendly format. aac is a widely supported - audio codec, 44100 hz is a common frequency, and -ac 1 specifies the first version of the AAC spec for compatibility purposes.
- -f flv wraps the video in an flv format container for maximum compatibility with RTMP.

### Закинути чергу відео
```
ffmpeg -re -f concat -i media_queue.txt -c:v libx264 -c:a aac -ar 44100 -ac 2 -f flv rtmp://localhost:1935/stream/radio
```

Приклад txt файлу
```
ffconcat version 1.0
file video1x.mp4
file video2x.mp4
file video3x.mp4
file video4x.mp4
file video5x.mp4
```

### Обробка відео для нормальної роботи ffconcat
```
ffmpeg -i video1.mp4 -vcodec libx264 -vf fps=30 -video_track_timescale 60000 video1x.mp4
```

### HLS-стрім (для програвання в HLS плеєрі)
```
http://localhost:8080/live/radio.m3u8
```

### Локальний тест HLS
```
http://localhost:8080/player.html?url=http://localhost:8080/live/radio.m3u8
```