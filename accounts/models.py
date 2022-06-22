from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models

from scraping.models import City, Language


class MyUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, verbose_name='Email')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Город')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, blank=True, null=True,
                                 verbose_name='Язык программирования')
    send_email = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
