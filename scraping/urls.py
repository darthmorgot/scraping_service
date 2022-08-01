from django.urls import path

from scraping.views import home_view, list_view, detail_view, DetailPageView, ListPageView


urlpatterns = [
    # path('detail/<int:pk>/', detail_view, name='detail'),
    # path('list/', list_view, name='list'),
    path('detail/<int:pk>/', DetailPageView.as_view(), name='detail'),
    path('list/', ListPageView.as_view(), name='list'),
    path('', home_view, name='home'),
]
