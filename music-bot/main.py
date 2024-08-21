import asyncio
import subprocess

# Базова директорія для mp3 файлів
base_directory = 'music-bot/music/'

# Асинхронна функція для програвання музики
async def play_music():
    # RTMP URL для стріму
    rtmp_url = 'rtmp://localhost:1935/stream/radio'

    # Програвання рандомної музики
    music_command = [
      'ffmpeg', '-re', '-f', 'concat', '-i', base_directory + 'media_queue.txt',
      '-c:v', 'libx264', '-c:a', 'aac', '-ar', '44100', '-ac', '2', '-f', 'flv', rtmp_url
    ]
    subprocess.run(music_command)

# Асинхронний запуск
async def main():
    await play_music()

asyncio.run(main())
