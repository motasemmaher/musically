from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Album(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    artlist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=250)
    genre = models.CharField(max_length=250)   
    album_logo = models.FileField()

    def get_absolute_url(self):
       return reverse('muisc:detail', kwargs={"pk": self.pk})

    def __str__(self):
        return (self.artlist+"  "+self.album_title+"  "+self.genre)
    

class Song(models.Model):
    album = models.ForeignKey(Album,on_delete=models.CASCADE)
    audio_file =models.FileField()
    song_title = models.CharField(max_length=250)
    is_favorite=models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('muisc:detail', kwargs={"pk": album.pk})

    def __str__(self):
        return (self.song_title)

