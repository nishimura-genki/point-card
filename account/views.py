from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import resolve_url, redirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import DeletionMixin
from .forms import UserCreateForm, CustomerCreateForm, ShopCreateForm, CustomerProfileUpDateForm, ShopProfileUpDateForm
from .models import Shop, Customer


class Top(generic.TemplateView):
    template_name = 'top.html'


class Customer_Top(generic.TemplateView):
    template_name = 'customer_top.html'


class Shop_Top(generic.TemplateView):
    template_name = 'shop_top.html'


class CustomerSignUpView(generic.TemplateView):
    template_name = 'registration/signup_form.html'
    success_url = 'customer_top'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['user_form'] = UserCreateForm(prefix='user')
        context['customer_form'] = CustomerCreateForm(prefix='customer')
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user_form = UserCreateForm(request.POST, prefix='user')
        customer_form = CustomerCreateForm(request.POST, prefix='customer')
        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save(commit=False)
            user.is_customer = True
            customer = customer_form.save(commit=False)
            customer.user = user
            user.save()
            user_form.save_m2m()
            customer.save()
            customer_form.save_m2m()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(user_form=user_form, customer_form=customer_form))


class ShopSignUpView(generic.TemplateView):
    template_name = 'registration/signup_form.html'
    success_url = 'shop_top'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['user_form'] = UserCreateForm(prefix='user')
        context['shop_form'] = ShopCreateForm(prefix='shop')
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user_form = UserCreateForm(request.POST, prefix='user')
        shop_form = ShopCreateForm(request.POST, prefix='shop')
        if user_form.is_valid() and shop_form.is_valid():
            user = user_form.save(commit=False)
            user.is_shop = True
            shop = shop_form.save(commit=False)
            customer.user = user
            user.save()
            user_form.save_m2m()
            shop.save()
            shop_form.save_m2m()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(user_form=user_form, shop_form=shop_form))


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'registration/profile.html'

    def get_context_data(self, *args, **kwargs):
        """
        Contextにuser, profile, profile_type を追加
        """
        user = self.request.user
        if user.is_customer:
            profile_type = 'Customer'
            profile = Customer.objects.get(user=user)
        elif user.is_shop:
            profile_type = 'Shop'
            profile = Shop.objects.get(user=user)
        else:
            profile_type = 'unknown'
            profile = None
        return super().get_context_data(user=user, profile=profile, profile_type=profile_type)


class CustomerProfileUpDateView(LoginRequiredMixin, generic.UpdateView):
    model = Customer
    form_class = CustomerProfileUpDateForm
    template_name = 'register/customer_form.html'

    def get_success_url(self):
        return resolve_url('register:customer_profile', pk=self.kwargs['pk'])


class ShopProfileUpDateView(LoginRequiredMixin, generic.UpdateView):
    model = Shop
    form_class = ShopProfileUpDateForm
    template_name = 'register/shop_form.html'

    def get_success_url(self):
        return resolve_url('register:shop_profile', pk=self.kwargs['pk'])


class DeleteView(LoginRequiredMixin, DeletionMixin, TemplateResponseMixin, generic.View):
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('accounts:delete-complete')

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return self.render_to_response(context=None)
