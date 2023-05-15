from . models import *
from django . forms import *


class CreateMusicForm(ModelForm):
    class Meta:
        model = Music

        fields = ['name_of_song', 'genre', 'music_file', 'cover_image', 'text_of_song']

        labels = {
            'genre': 'Genre of song:',
            'music_file': 'Select music file(.mp3):',
            'cover_image': 'Select music cover image:',
            'text_of_song': 'Lyric of song:'
        }

        widgets = {
            "music_file": FileInput(attrs={
                'class': 'form-control',
            }),
            "cover_image": FileInput(attrs={
                'class': 'form-control',
            }),
            "name_of_song": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name of song'
            }),
            "text_of_song": Textarea(attrs={
                'class': 'form-control',
            }),
        }

    def clean(self):
        name_of_song = self.cleaned_data['name_of_song']

        if len(name_of_song) > 100:
            raise ValidationError('Name of song must be least at 100 characters')


class CreateReviewForm(ModelForm):
    class Meta:
        model = Review

        fields = ['text', 'rating']

        widgets = {
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Comment'
            }),
            'rating': Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select a rating'
            })
        }
