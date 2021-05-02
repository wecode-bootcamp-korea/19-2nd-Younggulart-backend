from django.db import models

class Order(models.Model):
    user       = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    status     = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True)
    address    = models.ForeignKey('users.Address', on_delete=models.SET_NULL, null=True)
    art        = models.ManyToManyField('arts.Art', through='OrderArt')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'

class OrderArt(models.Model):
    order          = models.ForeignKey(Order, on_delete=models.CASCADE)
    art            = models.ForeignKey('arts.Art', on_delete=models.CASCADE)
    paid_price     = models.DecimalField(max_digits=10, decimal_places=2)
    frame_material = models.ForeignKey('FrameMaterial', on_delete=models.SET_NULL, null=True, blank=True)
    frame_size     = models.ForeignKey('FrameSize', on_delete=models.SET_NULL, null=True, blank=True)
    frame_price    = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    message        = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'order_arts'

class FrameMaterial(models.Model):
    name      = models.CharField(max_length=45)
    image_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'frame_materials'

class FrameSize(models.Model):
    name            = models.CharField(max_length=45)
    price_rise_rate = models.DecimalField(max_digits=3, decimal_places=2)
    thickness_cm    = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        db_table = 'frame_sizes'

class Status(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'status'