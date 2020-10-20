from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone


class UserManager(UserManager):
    def _create_user(self, email, sex, age, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, sex=sex,
                          age=age, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, sex, age, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)  # 管理者権限なし
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, sex, age, password, **extra_fields)

    def create_superuser(self, email, sex, age, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)  # 管理者権限あり
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, sex, age, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    SEX_CHOICES = (
        ('man', '男性'),
        ('woman', '女性'),
        ('other', 'その他'),
    )

    email = models.EmailField(_('email address'), unique=True)
    sex = models.IntegerField(_(' sex '), choices=SEX_CHOICES,
                              null=True, blank=True)
    age = models.IntegerField(_(' age '), null=True, blank=True, unique=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

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
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
