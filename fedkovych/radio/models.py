from django.db import models
import os
from django.conf import settings

# class Song(models.Model):
#     title = models.CharField(max_length=255)
#     mp3_file = models.FileField(upload_to=os.path.join(os.path.dirname(settings.BASE_DIR), 'music-bot/music/'))
#     date_added = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title

#     class Meta:
#         verbose_name = 'Пісня'
#         verbose_name_plural = 'Пісні'
#         ordering = ['-date_added']

class Video(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name='Назва пісні')
    mp4_file = models.FileField(upload_to='music/', verbose_name='Файл')
    is_converted = models.BooleanField(default=False)
    duration_seconds = models.IntegerField(null=True)
    date_added = models.DateTimeField(auto_now_add=True,verbose_name='Дата додавання')

    def save(self, *args, **kwargs):
        if not self.title and self.mp4_file:
            self.title = os.path.splitext(os.path.basename(self.mp4_file.name))[0]
        super(Video, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Відео'
        verbose_name_plural = 'Відео'
        ordering = ['-date_added']