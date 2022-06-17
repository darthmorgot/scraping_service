from django.shortcuts import render
from scraping.models import Vacancy


def home_view(request):
    vacancies = Vacancy.objects.all()
    context = {
        'vacancies': vacancies
    }
    return render(request, 'scraping/index.html', context=context)
