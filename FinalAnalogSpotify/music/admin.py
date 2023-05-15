from django.contrib import admin
from django.utils.safestring import mark_safe

from music.models import *


class MusicAdmin(admin.ModelAdmin):
    list_display = ('name_of_song', 'author_name', 'time_length', 'get_html_cover_image')
    prepopulated_fields = {'slug': ('name_of_song',)}

    def get_html_cover_image(self, object):
        if object.cover_image:
            return mark_safe(f"<img src='{object.cover_image.url}' width=50>")

    get_html_cover_image.short_description = "image"


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name_of_album', 'author_of_album', 'get_html_img')
    prepopulated_fields = {'slug': ('name_of_album',)}

    def get_html_img(self, object):
        if object.img:
            return mark_safe(f"<img src='{object.img.url}' width=50>")

    get_html_img.short_description = "image"


admin.site.register(Genre)
admin.site.register(Music, MusicAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Review)

admin.site.site_title = 'Ethereal admin'
admin.site.site_header = 'ethereal admin'
