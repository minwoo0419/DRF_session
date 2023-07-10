from django.db import models

# Create your models here.
def image_upload_path(instance, filename):
    return f'{instance.pk}/{filename}'

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

class Album(models.Model):
    id = models.AutoField(primary_key=True)
    artist = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    year = models.PositiveIntegerField(default=2023)
    description = models.TextField(max_length=200)
    tag = models.ManyToManyField(Tag, blank=True)


class Track(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=50)
    album = models.ForeignKey(Album, blank=False, null=False, on_delete=models.CASCADE, related_name='tracks')

class AlbumImage(models.Model):
    album = models.ForeignKey(Album, blank=False, null=False, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=image_upload_path, blank=True, null=True)