from django.contrib import admin
from .models import Video #,Song

# @admin.register(Song)
# class SongAdmin(admin.ModelAdmin):
#     list_display = ['title', 'date_added']
#     search_fields = ['title']
#     date_hierarchy = 'date_added'
#     list_filter = ['date_added']


@admin.register(Video)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_added']
    search_fields = ['title']
    date_hierarchy = 'date_added'
    list_filter = ['date_added']