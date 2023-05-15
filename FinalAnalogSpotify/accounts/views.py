from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView


from accounts.forms import ArtistProfileForm
from accounts.models import *


def register(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            user = CustomUser.objects.create_user(username=username, password=password1, email=email)
            user.save()
            new_user = authenticate(username=username,
                                    password=password1,
                                    )
            login(request, new_user)
            print("User created")
        else:
            print("User not created")
            messages.info(request, 'Password not matching')

        return redirect('/home')
    else:
        return render(request, 'accounts/register.html')


def signin(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid credential')
            return redirect('login')

    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


class CreateArtistProfileView(CreateView):

    model = ArtistProfile
    template_name = 'accounts/register_artist.html'
    form_class = ArtistProfileForm

    def form_valid(self, form):
        form.instance.user = self.request.user

        # cur = connection.cursor()
        # connection.autocommit = False
        # data = dict(p_user_id=self.request.user.id)
        # sql = 'UPDATE ACCOUNTS_CUSTOMUSER SET authorcheck = 1 ' \
        #       'WHERE id = :p_user_id'
        # cur.execute(sql, data)
        # connection.commit()

        return super().form_valid(form)

    success_url = reverse_lazy('browse_music')


'''def registerArtist(request):

    if request.method == 'POST':

        artist_name = request.POST['artist_name']
        birthdate = request.POST['birthdate']
        country = request.POST['country']
        artist_img = request.POST.get('artist_img')
        artist_poster_img = request.POST.get('artist_poster_img')
        user_id = request.user

        cur = connection.cursor()
        connection.autocommit = False
        data = dict(p_name=artist_name, p_img=artist_img, p_poster_img=artist_poster_img, p_bday=birthdate, p_country=country, p_user_id=user_id)
        sql =  'INSERT INTO ACCOUNTS_ARTISTPROFILE (ARTIST_NAME, ARTIST_IMG, ARTIST_POSTER_IMG, BIRTHDATE, COUNTRY, USER_ID) VALUES (:p_name, :p_img, :p_poster_img, :p_bday, :p_country, :p_user_id)'
        cur.execute(sql, data)
        connection.commit()

        connection.autocommit = False
        cur.execute("UPDATE ACCOUNTS_CUSTOMUSER SET AUTHORCHECK = 1 WHERE ID = :p_user_id", p_user_id=user_id)
        connection.commit()
        cur.close()
        connection.close()
        return redirect('/home')

    else:
        return render(request, 'accounts/register_artist.html')
'''


