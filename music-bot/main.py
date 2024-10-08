import asyncio
import ffmpeg
import os
import psycopg2
import random
import time as t


base_directory = 'music/'
media_queue_file = 'media_queue.txt'
radio_schedule_file = 'radio_schedule.txt'
rtmp_url = 'rtmp://localhost:1935/stream/radio'

db_config = {
    'dbname': 'radio-db',
    'user': 'postgres',
    'password': 'root',
    'host': 'localhost',
    'port': '5433'
}


async def create_random_media_queue():
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute('SELECT title, mp4_file, duration_seconds FROM radio_video WHERE is_converted = True')
    media_info = [row for row in cur.fetchall()]
    cur.close()
    conn.close()
    random.shuffle(media_info)
    
    with open(f'{os.getcwd()}/{media_queue_file}', 'w', encoding='utf-8') as file:
        file.write('ffconcat version 1.0\n')
        for info in media_info:
            file.write(f'file {info[1]}\n')
    
    cur_time = int(t.time())
    with open(f'{os.getcwd()}/{radio_schedule_file}', 'w', encoding='utf-8') as file:
        for info in media_info:
            cur_time += int(info[2])
            file.write(f'{cur_time} {info[0]}\n')

async def process_files():
    with open(f'{os.getcwd()}/{radio_schedule_file}', 'w') as file:
        pass
    
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute('SELECT mp4_file FROM radio_video WHERE is_converted = False')
    media_info = [row[0] for row in cur.fetchall()]
    
    for file in media_info:
        probe = ffmpeg.probe(file)
        stream = next((stream for stream in probe['streams']), None)
        duration = int(float(stream['duration']))
        convert_video(file)
        cur.execute(f'UPDATE radio_video SET is_converted = True, duration_seconds = %s WHERE mp4_file = %s', (duration, file))
    
    if len(media_info) > 0:
        conn.commit()
    cur.close()
    conn.close()
    

def stream_queue():
    (
        ffmpeg
        .input(media_queue_file, f='concat', safe=0, re=None)
        .output(rtmp_url, vcodec='libx264', acodec='aac', ar=44100, ac=2, format='flv')
        .run()
    )

def convert_video(file: str):
    temp_file_name = '/temp_'.join(file.split('/'))
    (
        ffmpeg
        .input(file)
        .output(temp_file_name, vcodec='libx264', vf='fps=30', video_track_timescale=60000)
        .run()
    )
    os.remove(file)
    os.rename(temp_file_name, file)

async def play_music():
    while True:
        await process_files()
        await create_random_media_queue()
        stream_queue()

async def main():
    await play_music()

asyncio.run(main())
