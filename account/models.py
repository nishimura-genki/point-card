from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator


class UserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)

    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)

    is_customer = models.BooleanField(_('customer'), default=False)
    is_shop = models.BooleanField(_('shop'), default=False)

    date_joined = models.DateTimeField(_('date_joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=_(
        "user"), on_delete=models.CASCADE, primary_key=True)

    class Meta:
        abstract = True


class Customer(Profile):

    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    GENDER_CHOICES = (
        (1, '男性'),
        (2, '女性'),
        (3, 'その他'),
    )
    gender = models.IntegerField(_('gender'), choices=GENDER_CHOICES,
                                 null=True, blank=True)
    age = models.IntegerField(_('age'), null=True, blank=True,
                              validators=[MinValueValidator(1), MaxValueValidator(100)])

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)


class Shop(Profile):
    shop_name = models.CharField(_('shop name'), max_length=150)

    def __str__(self):
        return str(shop_name)
