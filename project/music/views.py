from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404
# Create your views here.

@api_view(['GET', 'POST'])
def album_list_create(request):
    if request.method == 'GET':
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(data=serializer.data)
    
    elif request.method == 'POST':
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            album = serializer.save()
            images = request.FILES.getlist('images')
            for image in images:
                AlbumImage.objects.create(album=album, image=image)
            description = request.data['description']
            words = description.split(' ')
            tag_list = []
            for w in words:
                if w[0] == '#':
                    tag_list.append(w[1:])
            for t in tag_list:
                try:
                    tag = get_object_or_404(Tag, name=t)
                except:
                    tag = Tag(name=t)
                    tag.save()
                album = get_object_or_404(Album, id=serializer.data['id'])
                album.tag.add(tag)
            album.save()
        return Response(data=AlbumSerializer(album).data)

@api_view(['GET', 'PATCH', 'DELETE'])
def album_detail_update_delete(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    if request.method == 'GET':
        serializer = AlbumSerializer(album)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = AlbumSerializer(instance=album, data=request.data)
        if serializer.is_valid():
            serializer.save()
            album = get_object_or_404(Album, id=serializer.data['id'])
            album.tag.clear()
            description = request.data['description']
            words = description.split(' ')
            tag_list = []
            for w in words:
                if w[0] == '#':
                    tag_list.append(w[1:])
            for t in tag_list:
                try:
                    tag = get_object_or_404(Tag, name=t)
                except:
                    tag = Tag(name=t)
                    tag.save()
                album.tag.add(tag)
            album.save()
            return Response(data=AlbumSerializer(album).data)
    elif request.method == 'DELETE':
        album.delete()
        data = {
            'delete_album':album_id
        }
        return Response(data)
        
@api_view(['GET', 'POST'])
def track_list_create(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    if request.method == 'GET':
        tracks = Track.objects.filter(album=album)
        serializer = TrackSerializer(tracks, many=True)
        return Response(data=serializer.data)
    
    elif request.method == 'POST':
        serializer = TrackSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(album=album)
            return Response(serializer.data)

@api_view(['GET', 'PATCH', 'DELETE'])
def track_detail_update_delete(request, album_id, track_id):
    album = get_object_or_404(Album, id=album_id)
    tracks = Track.objects.filter(album=album)
    track = get_object_or_404(tracks, id=track_id)
    if request.method == 'GET':
        serializer = TrackSerializer(track)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = TrackSerializer(instance=track, data=request.data)
        if serializer.is_valid():
            serializer.save(album=album)
            return Response(serializer.data)
    elif request.method == 'DELETE':
        track.delete()
        data = {
            'delete_track':track_id
        }
        return Response(data)

@api_view(['GET'])
def find_tag1(request, tag_name):
    f_tag = get_object_or_404(Tag, name=tag_name)
    if request.method == 'GET':
        album = Album.objects.filter(tag__in = [f_tag])
        serializer = AlbumSerializer(album, many=True)
        return Response(data=serializer.data)

@api_view(['POST'])
def find_tag2(request):
    f_tag = get_object_or_404(Tag, name=request.data['name'])
    album = Album.objects.filter(tag__in = [f_tag])
    serializer = AlbumSerializer(album, many=True)
    return Response(data=serializer.data)