from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.EmailField()
    profile_pic = models.ImageField(default='anonymous.png', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    # def clean(self):
    #     if self.phone in range(0,90):
    #         pass
    #     else:
    #         raise ValidationError('number not in range')


class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Out Door', 'Out Door'),
    )

    prod_name = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.CharField(max_length=20, choices=CATEGORY)
    description = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField('Tags')

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS)
    note = models.CharField(max_length=200)


    def __str__(self):
        return self.product.name




