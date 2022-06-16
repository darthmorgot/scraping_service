from django.db import models
from django.utils.text import slugify as django_slugify
from transliterate import slugify


class City(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=50, blank=True, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.name))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']


class Language(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=50, blank=True, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = django_slugify(str(self.name))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Язык програмиирования'
        verbose_name_plural = 'Языки программирования'
        ordering = ['name']
