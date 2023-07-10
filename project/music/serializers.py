from rest_framework import serializers
from .models import *

class AlbumImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, required=False)
    class Meta:
        model = AlbumImage
        fields = ['image']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class AlbumSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    tracks = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    def get_tracks(self, instance):
        serializer = TrackSerializer(instance.tracks, many=True)
        return serializer.data
    def get_tags(self, instance):
        tags = instance.tag.all()
        return [tag.name for tag in tags]
    def get_images(self, instance):
        image = instance.images.all() 
        return AlbumImageSerializer(instance=image, many=True).data
    class Meta:
        model = Album
        fields = ['id', 'artist', 'title', 'year', 'description', 'tracks', 'tags', 'images']

class TrackSerializer(serializers.ModelSerializer):
    album = serializers.SerializerMethodField()
    def get_album(self, instance):
        return instance.album.title
    class Meta:
        model = Track
        fields = ['album', 'number', 'title']
        read_only_fields = ['album']
