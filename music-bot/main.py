import asyncio
import ffmpeg
import os
import psycopg2
import random
import time as t
from dotenv import load_dotenv
from google.cloud import storage

load_dotenv()

base_directory = 'music/'
media_queue_file = 'media_queue.txt'
radio_schedule_file = 'radio_schedule.txt'
rtmp_url = 'rtmp://rtmp.pp.ua:1935/stream/radio'

db_config = {
    'dbname': os.getenv('DATABASE_NAME'),
    'user': os.getenv('DATABASE_USER'),
    'password': os.getenv('DATABASE_USER_PASSWORD'),
    'host': os.getenv('DATABASE_HOST'),
}

gcloud_bucket = os.getenv('GS_BUCKET_NAME')


async def create_random_media_queue():
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute('SELECT title, mp4_file, duration_seconds FROM radio_video WHERE is_converted = True')
    media_info = [row for row in cur.fetchall()]
    cur.close()
    conn.close()
    
    random.shuffle(media_info)
    
    tracks = []
    for i in range(0, 12):
        tracks.extend(media_info)
    
    with open(media_queue_file, 'w', encoding='utf-8') as file:
        file.write('ffconcat version 1.0\n')
        for info in tracks:
            file.write(f'file {info[1]}\n')
    
    delay = 15
    cur_time = int(t.time()) + delay
    with open(radio_schedule_file, 'w', encoding='utf-8') as file:
        for info in tracks:
            cur_time += int(info[2])
            file.write(f'{cur_time} {info[0]}\n')
    
    gcloud_upload(radio_schedule_file)

async def process_files():
    with open(f'{os.getcwd()}/{radio_schedule_file}', 'w') as file:
        pass
    
    gcloud_upload(radio_schedule_file)
    
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute('SELECT mp4_file FROM radio_video WHERE is_converted = False')
    media_info = [str(row[0]) for row in cur.fetchall()]
    
    for file in media_info:
        print(f'Downloading "{file}"...')
        gcloud_download(file)
        probe = ffmpeg.probe(file)
        stream = next((stream for stream in probe['streams']), None)
        duration = int(float(stream['duration']))
        if file.endswith('.mp4'):
            convert_video(file)
            print(f'Uploading "{file}"...')
            gcloud_upload(file)
        cur.execute(f'UPDATE radio_video SET is_converted = True, duration_seconds = %s WHERE mp4_file = %s', (duration, file))
    
    if len(media_info) > 0:
        conn.commit()
    
    cur.close()
    conn.close()

# Google Cloud

def gcloud_download(file):
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcloud_bucket)
    blob = bucket.blob(file)
    blob.download_to_filename(file)

def gcloud_upload(file):
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcloud_bucket)
    blob = bucket.blob(file)
    blob.upload_from_filename(file)

# FFmpeg

def stream_queue():
    (
        ffmpeg
        .input(media_queue_file, f='concat', safe=0, re=None)
        .output(rtmp_url, vcodec='libx264', acodec='aac', ar=44100, ac=2, ab='192k', format='flv')
        .run()
    )

def convert_video(file: str):
    temp_file_name = '/temp_'.join(file.split('/'))
    (
        ffmpeg
        .input(file)
        .output(temp_file_name, vcodec='libx264', vf='fps=30, scale=854:480', video_track_timescale=90000, acodec='aac', ar=44100, ac=2, ab='192k')
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
