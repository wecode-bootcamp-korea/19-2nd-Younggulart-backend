from django.db import models

class User(models.Model):
    email = models.EmailField(max_length=100)

    class Meta:
        db_table = 'users'

class Address(models.Model):
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    postal_code    = models.CharField(max_length=10)
    main_address   = models.CharField(max_length=100)
    detail_address = models.CharField(max_length=100)

    class Meta:
        db_table = 'addresses'