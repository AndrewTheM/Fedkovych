import asyncio
import ffmpeg
import os
import random


base_directory = 'music/'
media_queue_file = 'media_queue.txt'
rtmp_url = 'rtmp://localhost:1935/stream/radio'


async def play_music():
    while True:
        await create_random_media_queue()
        (
            ffmpeg
            .input(base_directory + media_queue_file, f='concat', re=None)
            .output(rtmp_url, vcodec='libx264', acodec='aac', ar=44100, ac=2, format='flv')
            .run()
        )

async def create_random_media_queue():
    dir = f'{os.getcwd()}/{base_directory}'
    media = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    if media_queue_file in media:
        media.remove(media_queue_file)
    random.shuffle(media)
    commands = ['ffconcat version 1.0']
    for file in media:
        commands.append(f'file {file}')
    with open(f'{dir}/{media_queue_file}', 'w') as file:
        for line in commands:
            file.write(f'{line}\n')

async def main():
    await play_music()

asyncio.run(main())
