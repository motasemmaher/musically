from django.conf.urls import include,url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from muisc import views
from django.contrib.auth.models import User


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^Musically/',include('muisc.urls')),
    url(r'^Album/',views.albumList.as_view()),
    url(r'^Song/',views.songList.as_view()),
    url(r'^User/',views.userList.as_view()),


]
urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
