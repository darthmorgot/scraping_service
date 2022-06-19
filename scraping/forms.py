from django import forms

from scraping.models import City, Language


class SearchForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name='slug', required=False, label='Город',
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    language = forms.ModelChoiceField(queryset=Language.objects.all(), to_field_name='slug', required=False,
                                      label='Язык программирования',
                                      widget=forms.Select(attrs={'class': 'form-control'}))
