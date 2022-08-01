from django import forms

from scraping.models import City, Language, Vacancy


class SearchForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name='slug', required=False, label='Город',
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    language = forms.ModelChoiceField(queryset=Language.objects.all(), to_field_name='slug', required=False,
                                      label='Язык программирования',
                                      widget=forms.Select(attrs={'class': 'form-control'}))


class CreateForm(forms.ModelForm):
    url = forms.CharField(label='URL', widget=forms.URLInput(attrs={'class': 'form-control'}))
    title = forms.CharField(label='Название вакансии', widget=forms.TextInput(attrs={'class': 'form-control'}))
    company = forms.CharField(label='Компания', widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Описание вакансии', widget=forms.Textarea(attrs={'class': 'form-control'}))
    city = forms.ModelChoiceField(queryset=City.objects.all(), label='Город',
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    language = forms.ModelChoiceField(queryset=Language.objects.all(), label='Язык программирования',
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Vacancy
        fields = '__all__'
