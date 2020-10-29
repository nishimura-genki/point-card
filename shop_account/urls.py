from django.urls import path
from django.views.generic import TemplateView
from .views import SignUpView, ProfileView, DeleteView

app_name = 'shop_account'
urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('delete_confirm/', TemplateView.as_view(template_name='registration/delete_confirm.html'),
         name='delete-confirmation'),
    path('delete_complete/', DeleteView.as_view(), name='delete-complete'),
]
