from django.db import models

class Auction(models.Model):
    start_date  = models.DateTimeField()
    end_date    = models.DateTimeField()
    location    = models.CharField(max_length=100)
    subscriber  = models.ManyToManyField('users.User', through='AuctionUser')
    latitude_x  = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    longitude_y = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    art         = models.ManyToManyField('arts.Art', through='AuctionArt')

    class Meta:
        db_table = 'auctions'

class AuctionArt(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    art     = models.ForeignKey('arts.Art', on_delete=models.CASCADE)

    class Meta:
        db_table = 'auction_arts'

class AuctionUser(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'auction_users'