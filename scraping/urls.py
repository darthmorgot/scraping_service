from django.urls import path

from scraping.views import home_view, list_view, detail_view, DetailPageView, ListPageView, CreatePageView, \
    UpdatePageView, DeletePageView

app_name = 'scraping'

urlpatterns = [
    # path('detail/<int:pk>/', detail_view, name='detail'),
    # path('list/', list_view, name='list'),
    path('detail/<int:pk>/', DetailPageView.as_view(), name='detail'),
    path('create/', CreatePageView.as_view(), name='create'),
    path('update/<int:pk>/', UpdatePageView.as_view(), name='update'),
    path('delete/<int:pk>/', DeletePageView.as_view(), name='delete'),
    path('list/', ListPageView.as_view(), name='list'),
    path('', home_view, name='home'),
]
