from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


app_name= 'muisc'

urlpatterns = [
    
    url (r'register/$',views.create_account,name="register"),
    # /muisc
    url(r'homepage/$',views.index, name='index'),
 
    #/muisc/Album_id/
    url(r'album/(?P<album_id>[0-9]+)/details/$',views.detailViews,name='detail'),

    # /add Album 
    url(r'album/add/$',views.create_album,name='album-add'),

    # /edit Album 
    url(r'album/(?P<pk>[0-9]+)/edit/$',views.AlbumUpdate.as_view(),name='album-update'),

    # /delete Album 
    url(r'album/(?P<pk>[0-9]+)/delete/$',views.AlbumDelete.as_view(),name='album-delete'),

    #add song 
    url(r'^(?P<album_id>[0-9]+)/create_song/$', views.create_song, name='create_song'),

    url(r'login/$',views.Login,name='login'),
    url(r'^$',views.logout_user.as_view(),name="logout_user"),
    url(r'song/$',views.songViews.as_view(),name='song'),

]