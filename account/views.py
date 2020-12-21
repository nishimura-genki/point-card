from account import qr_code
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.views.generic.edit import DeletionMixin, FormMixin
from django.shortcuts import render, resolve_url, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth import (
    get_user_model, logout as auth_logout,
)
from .models import Profile, Customer, Shop, PointCard, PointCardLog
from .forms import UserCreateForm, CustomerCreateForm, ShopCreateForm, CustomerProfileUpDateForm, ShopProfileUpDateForm, UsePointForm, AddPointForm, CashierForm, UseStampForm, AddStampForm, CustomizePointCardForm
User = get_user_model()
import datetime
from django.db.models import Q
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64


class ShopRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_shop:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class Top(generic.TemplateView):
    template_name = 'top.html'


class Shop_Top(generic.TemplateView):
    template_name = 'shop_top.html'


class MyPage(LoginRequiredMixin, generic.TemplateView):
    template_name = 'registration/mypage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class CustomerSignUpView(generic.TemplateView):
    template_name = 'registration/customer_signup.html'
    success_url = '/'

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
        Contextにuser, profile,  を追加
        """
        user = self.request.user
        if user.is_customer:
            profile = Customer.objects.get(user=user)
        elif user.is_shop:
            profile = Shop.objects.get(user=user)
        else:
            profile = None
        return super().get_context_data(user=user, profile=profile)


class CustomerProfileUpDateView(LoginRequiredMixin, generic.UpdateView):
    model = Customer
    form_class = CustomerProfileUpDateForm
    template_name = 'registration/customer_form.html'

    def get_success_url(self):
        return resolve_url('accounts:profile')

    def get_object(self):
        return self.request.user.customer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class ShopProfileUpDateView(LoginRequiredMixin, generic.UpdateView):
    model = Shop
    form_class = ShopProfileUpDateForm
    template_name = 'registration/shop_form.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user.shop

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class CustomizePointCardView(ShopRequiredMixin, generic.UpdateView):
    model = Shop
    form_class = CustomizePointCardForm
    template_name = 'account/customize_point_card_form.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user.shop

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class DeleteView(LoginRequiredMixin, DeletionMixin, TemplateResponseMixin, generic.View):
    template_name = 'registration/delete_confirm.html'
    success_url = reverse_lazy('accounts:delete-complete')

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return self.render_to_response(context=self.get_context_data())

    def get_context_data(self, **kwargs):
        context = {'user': self.request.user}
        return context


class CustomerRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_customer:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class PointCardListView(CustomerRequiredMixin, generic.ListView):
    template_name = 'account/point_card_list.html'
    model = PointCard

    def get_queryset(self):
        return super().get_queryset().filter(customer=Customer.objects.get(user=self.request.user))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class QRCodeView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'account/qrcode.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        qr = qr_code.QRCode.from_user(user)
        context.update({'user': user, 'data': str(qr)})
        return context


class MakePointCardView(CustomerRequiredMixin, ContextMixin, generic.View):

    def get(self, request, *args, **kwargs):
        class PointCardAlreadyExists(Exception):
            pass

        try:
            shop_user_id = self.kwargs.get('shop_user_id')
            shop_user = User.objects.get(pk=shop_user_id)
            if PointCard.objects.filter(shop=shop_user.shop, customer=request.user.customer).exists():
                raise PointCardAlreadyExists

            data = PointCard(customer=request.user.customer, shop=shop_user.shop,
                             has_point=shop_user.shop.has_point, has_stamp=shop_user.shop.has_stamp, point=0, number_of_stamps=0)

            data.save()

            return redirect('accounts:point_card_list')
        except PointCardAlreadyExists:
            context = self.get_context_data(message='このお店のポイントカードは作成済みです')
            return render(request, 'account/make_point_card_fail.html', context)
        except(TypeError, ValueError, Shop.DoesNotExist, User.DoesNotExist, PointCard.DoesNotExist):
            context = self.get_context_data()
            return render(request, 'account/make_point_card_fail.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['object_list'] = PointCard.objects.filter(
            customer=self.request.user.customer)
        return context


class PointCardMixin:
    """
    get_point_card(self)
    urlにUserのpkが含まれている場合にポイントカードを返す
    ログインされていてis_customerかis_shopが必要
    urlに含まれるUserとページを開くUserのタイプが異なることが必要
    """

    def get_point_card(self):
        if self.request.user.is_customer:
            customer = self.request.user.customer
            shop = Shop.objects.get(pk=self.kwargs.get('shop_user_id'))
        elif self.request.user.is_shop:
            customer = Customer.objects.get(
                pk=self.kwargs.get('customer_user_id'))
            shop = self.request.user.shop
        return PointCard.objects.get(shop=shop, customer=customer)


class UsePointView(PointCardMixin, ShopRequiredMixin, FormMixin, TemplateResponseMixin, generic.edit.ProcessFormView):
    success_url = reverse_lazy("shop_top")
    form_class = UsePointForm
    template_name = 'account/use_point.html'

    def get_initial(self):
        return {'points_point_card_has': int(self.get_point_card().point)}

    def form_valid(self, form):
        point_card = self.get_point_card()
        point_card.point -= form.cleaned_data['points_to_use']
        point_card.save()
        
        dt_now = datetime.datetime.now()
        pointcard_log = PointCardLog(customer=point_card.customer,shop=point_card.shop, time=dt_now.time() ,date=dt_now.date() ,action='use_point', point=-form.cleaned_data['points_to_use'])
        pointcard_log.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['points_point_card_has'] = self.get_point_card().point
        context['user'] = self.request.user
        return context

    def get(self, request, *args, **kwargs):
        point_card = self.get_point_card()
        if not point_card.has_point:
            return redirect('accounts:does_not_have_point')
        else:
            return super().get(self, request, *args, **kwargs)


class UseStampView(PointCardMixin, ShopRequiredMixin, FormMixin, TemplateResponseMixin, generic.edit.ProcessFormView):
    success_url = reverse_lazy("shop_top")
    form_class = UseStampForm
    template_name = 'account/use_stamp.html'

    def get_initial(self):
        return {'stamps_point_card_has': int(self.get_point_card().number_of_stamps)}

    def form_valid(self, form):
        point_card = self.get_point_card()
        point_card.number_of_stamps -= form.cleaned_data['stamps_to_use']
        point_card.save()

        dt_now = datetime.datetime.now()
        pointcard_log = PointCardLog(customer=point_card.customer,shop=point_card.shop, time=dt_now.time() ,date=dt_now.date() ,action='use_stamp', number_of_stamps=-form.cleaned_data['stamps_to_use'])
        pointcard_log.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stamps_point_card_has"] = self.get_point_card().number_of_stamps
        context['user'] = self.request.user
        return context

    def get(self, request, *args, **kwargs):
        point_card = self.get_point_card()
        if not point_card.has_stamp:
            return redirect('accounts:does_not_have_stamp')
        else:
            return super().get(self, request, *args, **kwargs)


class AddPointView(PointCardMixin, FormMixin, TemplateResponseMixin, generic.edit.ProcessFormView):
    success_url = reverse_lazy('shop_top')
    form_class = AddPointForm
    template_name = 'account/add_point.html'

    def form_valid(self, form):
        point_card = self.get_point_card()
        
        
        point_card.point += form.cleaned_data['points_to_add']
        point_card.save()

        dt_now = datetime.datetime.now()
        pointcard_log = PointCardLog(customer=point_card.customer,shop=point_card.shop, time=dt_now.time() ,date=dt_now.date() ,action='add_point', point=form.cleaned_data['points_to_add'])
        pointcard_log.save()

        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        point_card = self.get_point_card()

        if not point_card.has_point:
            return redirect('accounts:does_not_have_point')
        else:
            return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class AddStampView(PointCardMixin, FormMixin, TemplateResponseMixin, generic.edit.ProcessFormView):
    success_url = reverse_lazy('shop_top')
    form_class = AddStampForm
    template_name = 'account/add_stamp.html'

    def form_valid(self, form):
        point_card = self.get_point_card()
        point_card.number_of_stamps += form.cleaned_data['stamps_to_add']
        point_card.save()

        dt_now = datetime.datetime.now()
        pointcard_log = PointCardLog(customer=point_card.customer,shop=point_card.shop, time=dt_now.time() ,date=dt_now.date() ,action='add_stamp', number_of_stamps=form.cleaned_data['stamps_to_add'])
        pointcard_log.save()

        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        point_card = self.get_point_card()

        if not point_card.has_stamp:
            return redirect('accounts:does_not_have_stamp')
        else:
            return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class CashierView(PointCardMixin, FormMixin, TemplateResponseMixin, generic.edit.ProcessFormView):
    success_url = reverse_lazy('shop_top')
    form_class = CashierForm
    template_name = 'account/cashier.html'

    def get_initial(self):
        return {'points_point_card_has': int(self.get_point_card().point)}

    def form_valid(self, form):
        point_card = self.get_point_card()
        point_card.point += form.cleaned_data['price'] * \
            form.cleaned_data['point_rate']
        point_card.point -= form.cleaned_data['points_to_use']
        point_card.save()

        dt_now = datetime.datetime.now()
        pointcard_log = PointCardLog(customer=point_card.customer,shop=point_card.shop, time=dt_now.time() ,date=dt_now.date() ,action='cashier', point=form.cleaned_data['price'] * \
            form.cleaned_data['point_rate']-form.cleaned_data['points_to_use'])
        pointcard_log.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["points_point_card_has"] = self.get_point_card().point
        context['user'] = self.request.user
        return context


class ReadQRCodeView(generic.TemplateView):
    template_name = "account/read_qr_code.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class ProcessQRCodeView(ContextMixin, generic.View):
    def get(self, request, *args, **kwargs):
        data = request.GET['data']
        try:
            qr = qr_code.QRCode.from_str(data)
            context = {'qr':  qr}
            return render(request, 'account/process_qr_code.html', context)
        except qr_code.QRCodeError:
            return redirect('accounts:read_qr_code')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class DeletePointCardView(CustomerOfObjectRequiredMixin, DeletionMixin, TemplateResponseMixin, ContextMixin, generic.View):

    template_name = 'account/delete_point_card_confirm.html'
    success_url = reverse_lazy('accounts:delete_point_card_complete')

    def get_object(self):
        return PointCard.objects.get(pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        return self.render_to_response(context=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class PointCardLogListView(generic.ListView):
    model = PointCardLog
    template_name = 'account/point_card_log.html'
    

    def get_queryset(self):
        query_word = self.request.GET.get('query')
        object_list = PointCardLog.objects.filter(shop=self.request.user.shop).order_by('-date','-time')
 
        if query_word:
            object_list = object_list.filter(Q(action=query_word))
       
        return object_list
    
