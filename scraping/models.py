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


class Vacancy(models.Model):
    url = models.URLField(unique=True, db_index=True)
    title = models.CharField(max_length=250, verbose_name='Название вакансии')
    company = models.CharField(max_length=250, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание вакансии')
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name='vacancies_city', verbose_name='Город')
    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name='vacancies_lang',
                                 verbose_name='Язык программирования')
    timestamp = models.DateField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-timestamp']
