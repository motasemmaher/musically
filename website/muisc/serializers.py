from rest_framework import serializers
from .models import Album,Song
from django.contrib.auth.models import User

class Albumserializer(serializers.ModelSerializer):
    
   class Meta :
        model = Album
        fields = '__all__'

class Songserializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = '__all__'
class Userserializer(serializers.ModelSerializer):

    class Meta :
        model = User
        fields ='__all__'