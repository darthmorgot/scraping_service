from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

from scraping.forms import SearchForm
from scraping.models import Vacancy


def home_view(request):
    form = SearchForm()

    context = {'form': form}
    return render(request, 'scraping/index.html', context=context)


def list_view(request):
    form = SearchForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    page_vacancies = []

    if city or language:
        filtered = {}
        if city:
            filtered['city__slug'] = city
        if language:
            filtered['language__slug'] = language
        vacancies_list = Vacancy.objects.filter(**filtered)

        paginator = Paginator(vacancies_list, 10)
        page_number = request.GET.get('page')
        page_vacancies = paginator.get_page(page_number)

    context = {
        'vacancies': page_vacancies,
        'form': form,
        'city': city,
        'language': language,
    }
    return render(request, 'scraping/list.html', context=context)


def detail_view(request, pk):
    # obj = Vacancy.objects.get(pk=pk)
    obj = get_object_or_404(Vacancy, pk=pk)
    return render(request, 'scraping/detail.html', {'object': obj})


class DetailPageView(DetailView):
    queryset = Vacancy.objects.all()
    template_name = 'scraping/detail.html'


class ListPageView(ListView):
    model = Vacancy
    template_name = 'scraping/list.html'
    form = SearchForm()
    context_object_name = 'vacancies'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['city'] = self.request.GET.get('city')
        context['language'] = self.request.GET.get('language')
        context['form'] = self.form
        context['vacancies'] = context['page_obj']
        return context

    def get_queryset(self):
        city = self.request.GET.get('city')
        language = self.request.GET.get('language')
        page_vacancies = []
        if city or language:
            filtered = {}
            if city:
                filtered['city__slug'] = city
            if language:
                filtered['language__slug'] = language
            page_vacancies = Vacancy.objects.filter(**filtered)
        return page_vacancies
