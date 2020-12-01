from django.db import transaction
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Customer, Shop, PointCard
from django.utils.translation import ugettext_lazy as _
User = get_user_model()


class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        if User.USERNAME_FIELD == 'email':
            fields = ('email',)
        else:
            fields = ('username', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class CustomerCreateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'gender', 'age')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # @transaction.atomic
    # def save(self):
    #     user = super().save(commit=False)
    #     user.is_user = True
    #     user.save()
    #     return user


class ShopCreateForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('shop_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # @transaction.atomic
    # def save(self):
    #     user = super().save(commit=False)
    #     user.is_user = True
    #     user.save()
    #     return user


class CustomerProfileUpDateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'gender', 'age',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ShopProfileUpDateForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('shop_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class UsePointForm(forms.Form):
    points_point_card_has = forms.IntegerField(widget=forms.HiddenInput())
    points_to_use = forms.IntegerField(label='使うポイント数', min_value=0)
    error_messages = {'not_enough_points': _('ポイントが足りません')}

    def clean_points_to_use(self):
        points_to_use = self.cleaned_data.get("points_to_use")
        points_point_card_has = self.cleaned_data.get("points_point_card_has")
        if points_to_use > points_point_card_has:
            raise ValidationError(
                self.error_messages['not_enough_points'], code='not_enough_points')
        return points_to_use


class UseStampForm(forms.Form):
    stamps_point_card_has = forms.IntegerField(widget=forms.HiddenInput())
    stamps_to_use = forms.IntegerField(label='使うポイント数', min_value=0)
    error_messages = {'not_enough_stamps': _('スタンプが足りません')}

    def clean_stamps_to_use(self):
        stamps_to_use = self.cleaned_data.get("stamps_to_use")
        stamps_point_card_has = self.cleaned_data.get("stamps_point_card_has")
        if stamps_to_use > stamps_point_card_has:
            raise ValidationError(
                self.error_messages['not_enough_stamps'], code='not_enough_stamps')
        return stamps_to_use


class AddPointForm(forms.Form):
    points_to_add = forms.IntegerField(label='付与するポイント数', min_value=0)


class AddStampForm(forms.Form):
    stamps_to_add = forms.IntegerField(label='押すスタンプ数', min_value=0)

class CashierForm(forms.Form):
    points_point_card_has = forms.IntegerField(widget=forms.HiddenInput())
    price = forms.IntegerField(min_value=0, label='お会計額')
    point_rate = forms.FloatField(min_value=0, label="ポイント率")
    points_to_use = forms.IntegerField(label='使うポイント数', min_value=0)
    error_messages = {'not_enough_points': _('ポイントが足りません')}

    def clean_points_to_use(self):
        points_to_use = self.cleaned_data.get("points_to_use")
        points_point_card_has = self.cleaned_data.get("points_point_card_has")
        if points_to_use > points_point_card_has:
            raise ValidationError(
                self.error_messages['not_enough_points'], code='not_enough_points')
        return points_to_use
