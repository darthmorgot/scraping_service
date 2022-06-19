from django.shortcuts import render

from scraping.forms import SearchForm
from scraping.models import Vacancy


def home_view(request):
    form = SearchForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    vacancies = []

    if city or language:
        filtered = {}
        if city:
            filtered['city__slug'] = city
        if language:
            filtered['language__slug'] = language
        vacancies = Vacancy.objects.filter(**filtered)

    context = {
        'vacancies': vacancies,
        'form': form,
    }
    return render(request, 'scraping/index.html', context=context)
