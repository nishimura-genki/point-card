from django.urls import path
from .views import ItemFilterView, ItemUpdateView


urlpatterns = [
    path('', ItemFilterView.as_view(), name='index'),
    path('update/<int:pk>/', ItemUpdateView.as_view(), name='update')
]
