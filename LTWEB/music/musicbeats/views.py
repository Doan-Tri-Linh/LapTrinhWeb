from os import name
from django.core.checks import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from . models import History, Song, Song_channel,WatchLater,Channel,Category
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.db.models import Case, When, query
from django.http import HttpResponse
# Create your views here.


def index(request):
    category = Category.objects.all()
    song_trending = Song.objects.all().order_by('-viewer')[:4]
    song_today = Song.objects.all().order_by('-song_id')[:4]
    song_for_you = Song.objects.all().order_by('?')[:4]
    context = {
        'category':category,
        'song_trending':song_trending,
        'song_for_you':song_for_you,
        'song_today':song_today
    }
    return render(request, 'musicbeats/index.html', context)


def songs(request):
    category = Category.objects.all()
    song = Song.objects.all()
   
    context = {
        'song': song,
        'category': category
    }

    return render(request, 'musicbeats/songs.html', context)


def songpost(request, id):
    category = Category.objects.all()
    song = Song.objects.filter(song_id=id).first()
    song.viewer = song.viewer + 1  
    song.save()
    context = {
        'song': song,
        'category':category,
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

        channel = Channel(name=username)
        channel.save()

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

    return render(request, 'musicbeats/login.html')


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
            category = Category.objects.all()
            
            return render(request,f'musicbeats/songpost.html',{'song':song,'message':messages,'category':category})
            

      wl = WatchLater.objects.filter(user=request.user)
      ids = []
      for i in wl:
            ids.append(i.video_id)

      preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
      song = Song.objects.filter(song_id__in=ids).order_by(preserved)
      category = Category.objects.all()
      
      return render(request, "musicbeats/watchlater.html", {'song':song,'category':category} )


def logout_user(request):
    logout(request)
    return redirect("/")

def history(request):
    if request.method == "POST":
        user = request.user
        music_id = request.POST['music_id']
        history = History(user=user,music_id=music_id)
        history.save()
        return redirect(f'/songs/{music_id}')

    history = History.objects.filter(user=request.user)

    ids = []
    for i in history:
        ids.append(i.music_id)

    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved)
    category = Category.objects.all()
    return render(request,'musicbeats/history.html',{'history':song,'category':category})


def channel(request,channel):
    chan = Channel.objects.filter(name=channel).first()
    video_ids = str(chan.music).split(" ")[1:]
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(video_ids)])
    song = Song_channel.objects.filter(song_id__in=video_ids).order_by(preserved)  
 
    return render(request,'musicbeats/channel.html',{'channel':chan,'song_channel':song})



def upload(request):
    if request.method == "POST":
        name = request.POST['name']
        singer = request.POST['singer']
        image = request.FILES['image']
     
        song1 = request.FILES['file']
        
        song_model = Song_channel(name=name, singer=singer, image=image, song=song1,)
        song_model.save()
        
        print(song_model)
        music_id = song_model.song_id
        channel_find = Channel.objects.filter(name=str(request.user))
      
        print(channel_find)

        for i in channel_find:
            i.music += f" {music_id}"
            i.save()

    return render(request, "musicbeats/upload.html")

def search(request):
    category = Category.objects.all()
    query = request.GET.get("query")
    song = Song.objects.all()
    qs = song.filter(name__icontains=query)


    return render(request,'musicbeats/search.html',{'songs':qs,'query':query,'category':category})


def category_music(request,id,slug):

    category = Category.objects.all()
    song = Song.objects.filter(category_id =id)
 
   
    context = {
        'song':song,
        'category':category,

    }

    return render(request,'musicbeats/category_music.html',context)


def songpost_channel(request, id):

    song = Song_channel.objects.filter(song_id=id).first()
    context = {
        'song': song,    
    }
    return render(request, 'musicbeats/songpost_channel.html', context)


def delete(request,id):
    WatchLater.objects.filter(video_id=id).delete()
    return redirect("/watchlater")

def delete_channel(request,id1):
    Song_channel.objects.filter(song_id=id1).delete()
    return redirect("/channel")


def rank(request):
    category = Category.objects.all()
    song = Song.objects.all().order_by('-viewer')
   
    context = {
        'song': song,
        'category': category
    }

    return render(request,'musicbeats/rank.html',context)

