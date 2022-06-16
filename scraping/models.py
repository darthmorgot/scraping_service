from django.db import models
from transliterate import slugify


class City(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        pass

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']


class Language(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Язык програмиирования'
        verbose_name_plural = 'Языки программирования'
        ordering = ['name']
