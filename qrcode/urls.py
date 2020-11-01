from django.urls import path
from django.views.generic import TemplateView
app_name = "qrcode"

urlpatterns = [
    path('', TemplateView.as_view(
        template_name='qrcode/read_qr_test.html'), name='read_qr_test'),

]
