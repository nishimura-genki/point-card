from account import qr_code
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import DeletionMixin, FormMixin
from django.shortcuts import render, resolve_url, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth import (
    get_user_model, logout as auth_logout,
)
from .models import Profile, Customer, Shop, PointCard
from .forms import UserCreateForm, CustomerCreateForm, ShopCreateForm, CustomerProfileUpDateForm, ShopProfileUpDateForm, UsePointForm, AddPointForm, CashierForm
User = get_user_model()


class Top(generic.TemplateView):
    template_name = 'top.html'


class Customer_Top(generic.TemplateView):
    template_name = 'customer_top.html'


class Shop_Top(generic.TemplateView):
    template_name = 'shop_top.html'


class CustomerSignUpView(generic.TemplateView):
    template_name = 'registration/customer_signup.html'
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


class DeleteView(LoginRequiredMixin, DeletionMixin, TemplateResponseMixin, generic.View):
    template_name = 'registration/delete_confirm.html'
    success_url = reverse_lazy('accounts:delete-complete')

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return self.render_to_response(context=None)


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
        qr = qr_code.QRCode.from_user(self.request.user)
        return super().get_context_data(data=str(qr), **kwargs)

    def get_success_url(self):
        return resolve_url('register:shop_profile', pk=self.kwargs['pk'])


class MakePointCardView(CustomerRequiredMixin, generic.View):

    def get(self, request, *args, **kwargs):

        try:
            # context = {
            # 'shop_id': request.POST['shop_id'],
            # }
            # print(context['shop_id'])
            shop_user_id = self.kwargs.get('shop_user_id')
            shop_user = User.objects.get(pk=shop_user_id)

            data = PointCard(customer=request.user.customer, shop=shop_user.shop,
                             has_point=True, has_stamp=True, point=0, number_of_stamps=0)
            """
            has_point と has_stamp をshopの情報から組み込めるようにする
            """
            data.save()

            print(data.shop)

            return redirect('accounts:point_card_list')
        except(TypeError, ValueError, Shop.DoesNotExist, User.DoesNotExist, PointCard.DoesNotExist):
            print('Error')
            context = {'object_list': PointCard.objects.filter(
                customer=request.user.customer)}
            return render(request, 'account/make_point_card_fail.html', context)


class UsePointView(FormMixin, TemplateResponseMixin, generic.edit.ProcessFormView):
    success_url = reverse_lazy("shop_top")
    form_class = UsePointForm
    template_name = 'account/use_point.html'

    def get_initial(self):
        return {'points_point_card_has': int(PointCard.objects.get(pk=self.kwargs.get('pk')).point)}

    def form_valid(self, form):
        point_card = PointCard.objects.get(pk=self.kwargs.get('pk'))
        point_card.point -= form.cleaned_data['points_to_use']
        point_card.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["points_point_card_has"] = PointCard.objects.get(
            pk=self.kwargs.get('pk')).point
        return context


class AddPointView(FormMixin, TemplateResponseMixin, generic.edit.ProcessFormView):
    success_url = reverse_lazy('shop_top')
    form_class = AddPointForm
    template_name = 'account/add_point.html'

    def form_valid(self, form):
        point_card = PointCard.objects.get(pk=self.kwargs.get('pk'))
        point_card.point += form.cleaned_data['points_to_add']
        point_card.save()
        return super().form_valid(form)


class CashierView(FormMixin, TemplateResponseMixin, generic.edit.ProcessFormView):
    success_url = reverse_lazy('shop_top')
    form_class = CashierForm
    template_name = 'account/cashier.html'

    def get_initial(self):
        return {'points_point_card_has': int(PointCard.objects.get(pk=self.kwargs.get('pk')).point)}

    def form_valid(self, form):
        point_card = PointCard.objects.get(pk=self.kwargs.get('pk'))
        point_card.point += form.cleaned_data['price'] * \
            form.cleaned_data['point_rate']
        point_card.point -= form.cleaned_data['points_to_use']
        point_card.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["points_point_card_has"] = PointCard.objects.get(
            pk=self.kwargs.get('pk')).point
        return context


class ReadQRCodeView(generic.TemplateView):
    template_name = "account/read_qr_code.html"


class ProcessQRCodeView(generic.View):
    def get(self, request, *args, **kwargs):
        data = request.GET['data']
        try:
            qr = qr_code.QRCode.from_str(data)
            context = {'qr':  qr}
            return render(request, 'account/process_qr_code.html', context)
        except qr_code.QRCodeError:
            return redirect('accounts:read_qr_code')


class DeletePointCardView(CustomerOfObjectRequiredMixin, DeletionMixin, TemplateResponseMixin, generic.View):

    template_name = 'account/delete_point_card_confirm.html'
    success_url = reverse_lazy('accounts:delete_point_card_complete')

    def get_object(self):
        return PointCard.objects.get(pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        return self.render_to_response(context=None)
