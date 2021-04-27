from django.db import models

class Artist(models.Model):
    name              = models.CharField(max_length=100)
    profile_image_url = models.URLField(max_length=2000)
    introduction      = models.TextField()
    description       = models.TextField()
    type              = models.ManyToManyField('Type', through='ArtistType')
    created_at        = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'artists'

class ArtistImage(models.Model):
    artist    = models.ForeignKey(Artist, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'artist_images'
    
class Type(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'types'

class ArtistType(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    type   = models.ForeignKey(Type, on_delete=models.CASCADE)

    class Meta:
        db_table = 'artist_types'