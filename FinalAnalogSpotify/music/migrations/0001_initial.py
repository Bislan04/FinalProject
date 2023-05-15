# Generated by Django 4.2.1 on 2023-05-14 19:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import music.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover_image', models.ImageField(upload_to='genre_images/', verbose_name='Genre cover image')),
                ('background_color', models.CharField(max_length=100, verbose_name='Genre background color')),
                ('name_of_genre', models.CharField(max_length=100, verbose_name='Genre name')),
                ('description', models.TextField(verbose_name='Description of genre')),
            ],
            options={
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genres',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('rating', models.CharField(blank=True, choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)], max_length=250, null=True, verbose_name='Rating of review')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Created date of review')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author of review')),
            ],
            options={
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
            },
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('music_file', models.FileField(upload_to='musics/', validators=[music.validators.validate_is_audio], verbose_name='Music File')),
                ('cover_image', models.ImageField(upload_to='music_images/')),
                ('name_of_song', models.CharField(max_length=250, verbose_name='Music name')),
                ('time_length', models.DecimalField(blank=True, decimal_places=2, max_digits=20)),
                ('release_date', models.DateField(auto_now_add=True, verbose_name='Release date')),
                ('text_of_song', models.TextField(blank=True, null=True, verbose_name='Text of song')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('author_name', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='authors', to='accounts.artistprofile', verbose_name='Select a author')),
                ('genre', models.ManyToManyField(to='music.genre', verbose_name='Genre of music')),
                ('like_music', models.ManyToManyField(blank=True, null=True, related_name='like_music', to=settings.AUTH_USER_MODEL, verbose_name='Do you like this music?')),
            ],
            options={
                'verbose_name': 'Music',
                'verbose_name_plural': 'Musics',
            },
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='album_images/', verbose_name='Album Image')),
                ('name_of_album', models.CharField(max_length=250, verbose_name='Album name')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Date')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('add_music', models.ManyToManyField(to='music.music', verbose_name='Add music')),
                ('author_of_album', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_albums', to='accounts.artistprofile', verbose_name='Author of album')),
                ('like_album', models.ManyToManyField(blank=True, null=True, related_name='like_album', to=settings.AUTH_USER_MODEL, verbose_name='Do you like this album?')),
            ],
            options={
                'verbose_name': 'Album',
                'verbose_name_plural': 'Albums',
                'ordering': ['name_of_album'],
            },
        ),
    ]
