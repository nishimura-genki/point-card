from django.shortcuts import render
from django.contrib.auth import (get_user_model, logout as auth_logout,)
from django.views import generic
from .forms import UserCreateForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()


class Shopper_Top(generic.TemplateView):
    template_name = 'shopper_top.html'


class SignUpView(generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ProfileView(LoginRequiredMixin, generic.View):

    def get(self, *args, **kwargs):
        return render(self.request, 'registration/profile.html')


class DeleteView(LoginRequiredMixin, generic.View):

    def get(self, *args, **kwargs):
        user = User.objects.get(email=self.request.user.email)
        user.is_active = True
        user.save()
        auth_logout(self.request)
        return render(self.request, 'registration/delete_complete.html')
