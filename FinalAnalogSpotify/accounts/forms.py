from . models import *
from django . forms import *


class ArtistProfileForm(ModelForm):
    class Meta:
        model = ArtistProfile

        fields = ['artist_name', 'birthdate', 'country', 'artist_img', 'artist_poster_img']
