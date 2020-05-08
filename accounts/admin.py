from atexit import register

from django.contrib import admin
from.models import *


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    True

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    True
