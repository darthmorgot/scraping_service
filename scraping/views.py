from django.shortcuts import render
from scraping.models import Vacancy


def home_view(request):
    # print(request.GET)
    city = request.GET.get('city')
    language = request.GET.get('language')
    vacancies = []

    if city or language:
        filtered = {}
        if city:
            filtered['city__name'] = city
        if language:
            filtered['language__name'] = language
        vacancies = Vacancy.objects.filter(**filtered)

    context = {
        'vacancies': vacancies
    }
    return render(request, 'scraping/index.html', context=context)
