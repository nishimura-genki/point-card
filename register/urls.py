from django.contrib import admin
from django.urls import path, include
from account import views

urlpatterns = [
    path('', views.Top.as_view(), name='top'),
    path('customer_top/', views.Customer_Top.as_view(), name='customer_top'),
    path('shop_top/', views.Shop_Top.as_view(), name='shop_top'),
    path('admin/', admin.site.urls),
    path('accounts/', include('account.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
