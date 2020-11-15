from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import DeletionMixin
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth import (
    get_user_model, logout as auth_logout,
)
from .forms import UserCreateForm, CustomerCreateForm, ShopCreateForm
from .models import Profile, Customer, Shop, PointCard
from django.shortcuts import redirect

User = get_user_model()


class Top(generic.TemplateView):
    template_name = 'top.html'


class User_Top(generic.TemplateView):
    template_name = 'user_top.html'


class SignUpView(generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class CustomerSignUpView(generic.TemplateView):
    template_name = 'registration/customer_signup.html'
    success_url = 'top'

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
    template_name = 'registration/shop_signup.html'
    success_url = 'top'

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
            shop.user = user
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


class DeleteView(LoginRequiredMixin, DeletionMixin, TemplateResponseMixin, generic.View):
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('accounts:delete-complete')

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return self.render_to_response(context=None)


class CustomerRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission
        if not request.user.is_customer:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class PointCardListView(CustomerRequiredMixin, generic.ListView):
    template_name = 'account/point_card_list.html'
    model = PointCard

    def get_queryset(self):
        return super().get_queryset().filter(customer=Customer.objects.get(user=self.request.user))


class CustomerOfObjectRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_customer:
            return self.handle_no_permission()
        if not self.get_object().customer == request.user.customer:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class PointCardDetailView(CustomerOfObjectRequiredMixin, generic.DetailView):
    model = PointCard
    template_name = 'account/point_card_detail.html'


class QRCodeView(CustomerRequiredMixin, generic.TemplateView):
    template_name = 'account/qrcode.html'
    def get_context_data(self, **kwargs):

        return super().get_context_data(data=self.request.user.customer.pk, **kwargs)
