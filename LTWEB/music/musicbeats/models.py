from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
# Create your models here.


class Category(MPTTModel):
     parent = TreeForeignKey('self', blank=True, null=True,
                             related_name='children', on_delete=models.CASCADE)
     title = models.CharField(max_length=50)
     slug = models.SlugField(null=False, unique=True)

     def __str__(self):
         return self.title

     class MPPTMeta:
         order_insertion_by =['title']
    




class Song(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #many to one relation with Category
    song_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    singer = models.CharField(max_length=200)
    tags = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')  
    song = models.FileField(upload_to='images')
    

    def __str__(self) :
        return self.name

class WatchLater(models.Model):
    
    watch_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=1000,default="")


class History(models.Model):
    hist_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=CASCADE)
    music_id = models.CharField(max_length=1000,default="")


class Channel(models.Model):
    channel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    music = models.CharField(max_length=1000)
    
     
