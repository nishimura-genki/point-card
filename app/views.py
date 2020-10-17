from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .forms import ItemForm
from django_filters.views import FilterView
from .models import Item


# Create your views here.

class ItemFilterView(LoginRequiredMixin, FilterView):
    model = Item


# 更新画面
class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')
