from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('customer_signup/', views.CustomerSignUpView.as_view(),
         name='customer_signup'),
    path('shop_signup/', views.ShopSignUpView.as_view(), name='shop_signup'),
    path('delete_confirm', views.DeleteView.as_view(), name='delete-confirmation'),
    path('delete_complete', TemplateView.as_view(
        template_name="registration/delete_complete.html"), name='delete-complete'),
]
