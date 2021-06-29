from django.core.checks import messages
from django.shortcuts import render
from . models import Song,WatchLater
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.db.models import Case, When
from django.http import HttpResponse
# Create your views here.


def index(request):

    song = Song.objects.all()
    context = {
        'song': song
    }
    return render(request, 'musicbeats/index.html', context)


def songs(request):
    song = Song.objects.all()
    context = {
        'song': song
    }

    return render(request, 'musicbeats/songs.html', context)


def songpost(request, id):
    song = Song.objects.filter(song_id=id).first()
    context = {
        'song': song
    }
    return render(request, 'musicbeats/songpost.html', context)


def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.save()
        user = authenticate(username=username, password=pass1)
        from django.contrib.auth import login
        login(request, user)

        return redirect('/')

    return render(request, 'musicbeats/signup.html',)


def login(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        from django.contrib.auth import login
        login(request, user)

        return redirect("/")

    return render(request, 'musicbeats/login.html',)


def watchlater(request):
      if request.method == "POST":
            user = request.user
            video_id = request.POST['video_id']

            watch = WatchLater.objects.filter(user=user)

            for i in watch:
                  if video_id == i.video_id:
                        messages = "Your video is alredy added"
                        break
            else:
                  
                  watchlater = WatchLater(user=user,video_id=video_id)
                  watchlater.save()
                  messages = "Your video is succesfuly added"
            song = Song.objects.filter(song_id=video_id).first()
            
            return render(request,f'musicbeats/songpost.html',{'song':song,'message':messages})
            

  
      return render(request, "musicbeats/watchlater.html")
