from django.views import generic
from django.views.generic.edit import CreateView ,UpdateView,DeleteView
from django.shortcuts import render , get_object_or_404,redirect
from django.views.generic import View
from .models import Album ,Song
from django.db.models import Q
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from .forms import SongForm,AlbumForm,UserForm
from django.contrib.auth.models import User
from .serializers import Albumserializer ,Songserializer,Userserializer
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate, login,logout


class albumList (APIView):

    def get(self,request):
        album =Album.objects.all()
        serializer = Albumserializer(album,many=True)  
        return Response(serializer.data)

    def post(self,request):
        data = JSONParser().parse(request)
        serializer = Albumserializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
         
class songList (APIView):

    def get(self,request):
        song =Song.objects.all()
        serializer = Songserializer(song,many=True)  
        return Response(serializer.data , status=201)
    
    def post(self,request):
        data = JSONParser().parse(request)
        serializer = Songserializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)




def index(request):
    if not request.user.is_authenticated:
        return render(request, 'muisc/login.html')
    else:
        albums = Album.objects.filter(user=request.user)
        song_results = Song.objects.all()
        query = request.GET.get("q")
        if query:
            albums = albums.filter(
                Q(album_title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
            song_results = song_results.filter(
                Q(song_title__icontains=query)
            ).distinct()
            return render(request, 'muisc/index.html', {
                'user':request.user,
                'all_album': albums,
                'songs': song_results,
            })
        else:
            return render(request, 'muisc/index.html', {'all_album': albums})
class logout_user(View):
    def get(self,request):
        request.user.is_active=False
        logout(request)
        form = UserForm(request.POST or None)

        context = {
            "form": form,
        }
        return render(request, 'muisc/login.html', context)

class userList (APIView):
                    def get(self,request):
                        users =User.objects.all()
                        serializer = Userserializer(users,many=True)  
                        return Response(serializer.data)

                    def post(self,request):
                        data = JSONParser().parse(request)
                        serializer = Userserializer(data=data)
                        if serializer.is_valid():
                            serializer.save()
                            return  JsonResponse(serializer.data, status=201)
                        return JsonResponse(serializer.errors, status=400)
def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                request.user.is_active=True
                login(request, user)
                albums = Album.objects.filter(user=request.user)

                

                return render(request, 'muisc/index.html', {'all_album': albums})
            else:
                return render(request, 'muisc/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'muisc/login.html', {'error_message': 'Invalid login'})
    return render(request, 'muisc/login.html')


def create_account(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        confirm_Password=form.cleaned_data['confirm_Password']
        if confirm_Password !=password:
            context={
                "form": form,
                'error_message':'enter the same password'
            }
            return render(request, 'muisc/register.html', context)
        user.set_password(password)
        user.save()
        
        user = authenticate(username=username, password=password)
        

        if user is not None: 
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'muisc/index.html', {'all_album': albums})
    context = {
        "form": form,
    }
    return render(request, 'muisc/register.html', context)
from django.views.generic.detail import DetailView

def detailViews(request,album_id):
    if not request.user.is_authenticated:
        return render(request, 'muisc/login.html')
    else:
        context={
            'album':Album.objects.filter(pk=album_id)
        }
        return render(request,'muisc/viewSong.html',context)
    return render(request, 'muisc/login.html')



    
class AlbumUpdate(UpdateView):
    model = Album
    fields  =['artlist','album_title','genre','album_logo']


class AlbumDelete(DeleteView):
    model = Album
#   success_url=reverse_lazy('music:index')

    

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['jpg','png','jpeg']



def create_album(request):
        form = AlbumForm(request.POST or None, request.FILES or None)
        if request.method == 'POST':
            vld_value = request.POST.get('validateValue')
            vld_id = request.POST.get('validateId')
            vld_error = request.POST.get('validateError')
            array_to_js = [vld_id, vld_error, False]
        
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.album_logo = request.FILES['album_logo']
            image_type =  album.album_logo.url.split('.')[-1]
            image_type = image_type.lower()
            if (image_type not in IMAGE_FILE_TYPES):
                context = {
                    'form': form,
                    'error_message': 'Image file must be jpg , png or jpeg',
                }
                return render(request,'muisc/album_form.html',context)
            album.save()
            return render(request,'muisc/Detail.html', {'album': album})
        context = {
            'form': form,
        }
        return render(request,'muisc/album_form.html',context)


def create_song(request, album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        albums_songs = album.song_set.all()
        for s in albums_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'muisc/create_song.html', context)
        song = form.save(commit=False)
        song.album = album
        song.audio_file = request.FILES['audio_file']
        file_type = song.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'album': album,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, or OGG',
            }
            return render(request,'muisc/create_song.html', context)

        song.save()
        return render(request,'muisc/Detail.html', {'album': album})
    context = {
        'album': album,
        'form': form,
    }
    return render(request,'muisc/create_song.html', context)

class songViews(generic.ListView):
    template_name = 'muisc/allSong.html'    
    context_object_name='all_song'

    def get_queryset(self):
        return Song.objects.all()


