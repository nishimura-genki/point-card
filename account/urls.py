from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('customer_signup/', views.CustomerSignUpView.as_view(), name='customer_signup'),
    path('shop_signup/', views.ShopSignUpView.as_view(), name='shop_signup'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
<<<<<<< HEAD
    path('signup/', TemplateView.as_view(template_name='registration/signup.html'), name='signup'),
    path('customer_signup/', views.CustomerSignUpView.as_view(),
         name='customer_signup'),
    path('shop_signup/', views.ShopSignUpView.as_view(), name='shop_signup'),
    path('delete_confirm', views.DeleteView.as_view(), name='delete-confirmation'),
    path('delete_complete', TemplateView.as_view(
        template_name="registration/delete_complete.html"), name='delete-complete'),
     path('point_card_list/', views.PointCardListView.as_view(),
         name='point_card_list'),
     path('point_card_detail/<int:pk>/',
          views.PointCardDetailView.as_view(), name='point_card_detail'),
    path('qrcode/', views.QRCodeView.as_view(), name='qrcode'),
=======
    path('customer_profile_update/', views.CustomerProfileUpDateView.as_view(),
         name='customer_profile_update'),
    path('shop_profile_update/', views.ShopProfileUpDateView.as_view(),
         name='shop_profile_update'),
    path('delete_confirm', TemplateView.as_view(
        template_name='registration/delete_confirm.html'), name='delete-confirmation'),
    path('delete_complete', views.DeleteView.as_view(), name='delete-complete'),
>>>>>>> shopaccount
]
