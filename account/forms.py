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

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_user = True
        user.save()
        return user


class ShopCreateForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('shop_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_user = True
        user.save()
        return user


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
    point_card_pk = forms.IntegerField(widget=forms.HiddenInput())
    points_to_use = forms.IntegerField()
    error_messages = {'not_enough_points': _('ポイントが足りません')}

    def clean_points_to_use(self):
        points_to_use = self.cleaned_data.get("points_to_use")
        point_card = PointCard.objects.get(
            pk=self.cleaned_data.get("point_card_pk"))
        if points_to_use > point_card.point:
            raise ValidationError(
                self.error_messages['not_enough_points'], code='not_enough_points')
        return points_to_use
