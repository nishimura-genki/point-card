from django.urls import path
from django.views.generic import TemplateView
app_name = "take_pic"

urlpatterns = [
    path('', TemplateView.as_view(
        template_name='take_pic/takepic.html'), name='takepic'),

]
