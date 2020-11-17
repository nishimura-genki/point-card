from django.contrib import admin

from .models import User, Customer, Shop, PointCard

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Shop)
admin.site.register(PointCard)
