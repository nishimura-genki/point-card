from django.contrib import admin

from .models import User, Customer, Shop, PointCard, PointCardLog

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Shop)
admin.site.register(PointCard)
admin.site.register(PointCardLog)
