from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from music.forms import CreateMusicForm, CreateReviewForm
from music.models import *


from django.views.generic import DetailView


@login_required
def index(request):
    message = 'Good Morning'

    all_music = Music.objects.all()
    all_albums = Album.objects.all()
    all_artists = ArtistProfile.objects.all()

    album_pop = set(all_albums.filter(add_music__genre__name_of_genre__exact='Pop'))
    album_hiphop = set(all_albums.filter(add_music__genre__name_of_genre__exact='Hip-hop').order_by('-name_of_album')[:45])
    album_rnb = set(all_albums.filter(add_music__genre__name_of_genre__exact='R&B').order_by('name_of_album')[:45])
    album_kpop = set(all_albums.filter(add_music__genre__name_of_genre__exact='K-Pop').order_by('name_of_album')[:45])

    context = {
        'all_music': all_music,
        'all_albums': all_albums[:4],
        'album_hiphop': album_hiphop,
        'album_rb': album_rnb,
        'album_pop': album_pop,
        'album_kpop': album_kpop,
        'message': message,
        'all_artists': all_artists
    }

    return render(request, 'music/home.html', context)


def AlbumDetailView(request, pk):
    album = get_object_or_404(Album, pk=pk)
    musics = album.add_music.all()

    liked_album = False
    if request.user.is_authenticated and album.like_album.filter(id=request.user.id).exists():
        liked_album = True

    context = {
        'album': album,
        'liked_album': liked_album
    }

    for music in musics:
        music.liked = music.like_music.filter(id=request.user.id).exists()

    return render(request, 'music/album_detail.html', context)


class ArtistDetailView(DetailView):
    model = ArtistProfile
    template_name = 'music/artist_detail.html'
    context_object_name = 'artist'

    def get_context_data(self, **kwargs):
        context = super(ArtistDetailView, self).get_context_data(**kwargs)
        genre_music = Music.objects.all()
        genre_album = Album.objects.all()
        genre_music_list = genre_music.filter(genre__music__author_name__exact=self.object.id).exclude(author_name__user__username__exact=self.object.user.username)[:5]
        genre_album_list = genre_album.filter(add_music__genre__music__author_name__exact=self.object.id).exclude(author_of_album__user__username__exact=self.object.user.username)[:5]
        context['music_list'] = Music.objects.filter(author_name__user__username__exact=self.object.user.username)
        context['album_list'] = set(Album.objects.filter(author_of_album__user__username__exact=self.object.user.username))

        context['similar_albums'] = set(genre_album_list)
        context['similar_musics'] = set(genre_music_list)

        return context


class MusicDetailView(DetailView):
    model = Music
    template_name = 'music/music_detail.html'
    context_object_name = 'music'

    def get_context_data(self, **kwargs):
        context = super(MusicDetailView, self).get_context_data(**kwargs)
        context['lyric_music'] = (Music.text_of_song, '.txt')
        context['music_list'] = Music.objects.filter(id__exact=self.object.id)
        return context


class GenreDetailView(DetailView):
    model = Genre
    template_name = 'music/genre_detail.html'
    context_object_name = 'genre'

    def get_context_data(self, **kwargs):
        context = super(GenreDetailView, self).get_context_data(**kwargs)
        context['genre_list'] = Music.objects.filter(genre__exact=self.object.id)
        return context


def search(request):

    search_item = ''
    if 'search' in request.GET:
        search_item = request.GET['search']
        genre_search = Q(name_of_genre__icontains=search_item)
        artist_search = Q(artist_name__icontains=search_item)
        all_genres = Genre.objects.filter(genre_search)
        all_artists = ArtistProfile.objects.filter(artist_search)[:5]
    else:
        all_genres = Genre.objects.all().order_by()[:5]
        all_artists = ArtistProfile.objects.all()[:5]

    context = {
        'all_genres': all_genres,
        'all_artists': all_artists,
        'search': search_item
    }

    return render(request, 'music/search.html', context)


def LikeAlbum(request, pk):
    album_like = get_object_or_404(Album, id=request.POST.get('album_id'))
    liked_album = False
    print(request.user.id)
    if album_like.like_album.filter(id=request.user.id).exists():
        album_like.like_album.remove(request.user)
        liked_album = False
    else:
        album_like.like_album.add(request.user)
        liked_album = True
    return HttpResponseRedirect(reverse('detail_album', args=[str(pk)]))


def RemoveLikeAlbum(request, pk):
    album_like = get_object_or_404(Album, id=request.POST.get('album_id'))
    if request.user in album_like.like_album.all():
        album_like.like_album.remove(request.user)

    return redirect('favorite_albums')


def RemoveLikeMusic(request, pk):
    music_like = get_object_or_404(Music, id=request.POST.get('music_id'))
    if request.user in music_like.like_music.all():
        music_like.like_music.remove(request.user)

    return redirect('favorite_musics')


def LikeMusic(request, pk):
    user = request.user
    music_like = get_object_or_404(Music, id=request.POST.get('music_like'))
    liked_music = False
    if user in music_like.like_music.all():
        music_like.like_music.remove(user)
        liked_music = False
    else:
        music_like.like_music.add(user)
        liked_music = True
    return redirect('detail_album', pk=Album.objects.filter(add_music=music_like).first().id)


def FavoriteMusics(request):
    all_musics = Music.objects.all()
    like_musics = Music.objects.filter(like_music__id=request.user.id)

    context = {
        'like_musics': like_musics,
        'all_musics': all_musics,
    }

    return render(request, 'music/favorite_musics.html', context)


def FavoriteAlbums(request):
    all_albums = Album.objects.all()
    like_albums = Album.objects.filter(like_album__id=request.user.id)

    context = {
        'like_albums': like_albums,
        'all_albums': all_albums,
    }

    return render(request, 'music/favorite_albums.html', context)


def AllGenres(request):
    all_genres = Genre.objects.all()

    context = {
        'all_genres': all_genres
    }

    return render(request, 'music/all_genres.html', context)


def AllArtists(request):
    all_artists = ArtistProfile.objects.all()

    context = {
        'all_artists': all_artists
    }

    return render(request, 'music/all_artists.html', context)


def AcceptCreated(request):
    return render(request, 'music/accept_created.html')


def CreateMusic(request):
    error = ''
    if request.method == 'POST':
        form = CreateMusicForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = request.user
            artist = ArtistProfile.objects.get(user=user_id)
            form.instance.author_name = artist
            form.save()
            return redirect('accept_created')
        else:
            error = 'The Form was incorrect!'

    form = CreateMusicForm(request.POST, request.FILES)

    context = {
        'form': form,
        'error': error
    }

    return render(request, 'music/create_music.html', context)


def CreateReview(request):

    reviews = Review.objects.all()

    error = ''
    form = CreateReviewForm
    if request.method == 'POST':
        form = CreateReviewForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('browse_music')
        else:
            error = 'The Form was Incorrect!'

    context = {
        'form': form,
        'error': error,
        'reviews': reviews
    }

    return render(request, 'music/create_review.html', context)


class ReviewDetail(DetailView):
    model = Review
    template_name = 'music/detail_review.html'
    context_object_name = 'review'
