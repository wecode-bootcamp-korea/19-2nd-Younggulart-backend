from django.db import models

class Art(models.Model):
    name          = models.CharField(max_length=100)
    price         = models.DecimalField(max_digits=10, decimal_places=2)
    description   = models.TextField()
    height_cm     = models.DecimalField(max_digits=6, decimal_places=2)
    width_cm      = models.DecimalField(max_digits=6, decimal_places=2)
    release_date  = models.DateField()
    thumbnail_url = models.URLField(max_length=2000)
    artist        = models.ForeignKey('artists.Artist', on_delete=models.SET_NULL, null=True)
    media         = models.ForeignKey('Media', on_delete=models.SET_NULL, null=True)
    theme         = models.ManyToManyField('Theme', through='ArtTheme')
    style         = models.ManyToManyField('Style', through='ArtStyle')
    paper         = models.ForeignKey('Paper', on_delete=models.SET_NULL, null=True)
    material      = models.ForeignKey('Material', on_delete=models.SET_NULL, null=True)
    color         = models.ManyToManyField('Color', through='ArtColor')
    views         = models.PositiveBigIntegerField()
    is_sold       = models.BooleanField(default=False)

    class Meta:
        db_table = 'arts'

class ArtImage(models.Model):
    art       = models.ForeignKey(Art, on_delete=models.SET_NULL, null=True)
    image_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'art_images'

class Media(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'medium'

class Paper(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'papers'

class Material(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'materials'

class Color(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'colors'

class ArtColor(models.Model):
    art   = models.ForeignKey(Art, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)

    class Meta:
        db_table = 'art_colors'

class Theme(models.Model):
    name  = models.CharField(max_length=45)
    media = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'themes'

class ArtTheme(models.Model):
    art   = models.ForeignKey(Art, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)

    class Meta:
        db_table = 'art_themes'

class Style(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'styles'

class ArtStyle(models.Model):
    art   = models.ForeignKey(Art, on_delete=models.CASCADE)
    style = models.ForeignKey(Style, on_delete=models.CASCADE)

    class Meta:
        db_table = 'art_styles'

class Banner(models.Model):
    image_url = models.URLField(max_length=2000)
    link_url  = models.URLField(max_length=2000)
    text      = models.CharField(max_length=45)

    class Meta:
        db_table = 'banners'