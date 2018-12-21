from django import forms
from .models import Album, Song
from django.contrib.auth.models import User





class AlbumForm(forms.ModelForm):
    conclusion = forms.CharField( widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}))
    class Meta:
        model = Album
        fields = ['artlist', 'album_title', 'genre', 'album_logo','conclusion']

class SongForm (forms.ModelForm):
    conclusion = forms.CharField( widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}))
    class Meta:
        model = Song
        fields  =['song_title','audio_file','conclusion']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_Password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'password','confirm_Password',]


