from django.urls import path

from scraping.views import home_view, list_view


urlpatterns = [
    path('list/', list_view, name='list'),
    path('', home_view, name='home'),
]
