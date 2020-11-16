<<<<<<< HEAD
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
=======
from django.db import transaction
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
>>>>>>> shopaccount
from .models import Customer, Shop

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
<<<<<<< HEAD
        fields = ('first_name', 'last_name', 'gender', 'age')
=======
        fields = ('first_name', 'last_name', 'gender', 'age',)
>>>>>>> shopaccount

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

<<<<<<< HEAD
=======
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_user = True
        user.save()
        return user

>>>>>>> shopaccount

class ShopCreateForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('shop_name',)
<<<<<<< HEAD
=======

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
>>>>>>> shopaccount

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
