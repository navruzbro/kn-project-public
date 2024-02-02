from django.urls import path

from filmnews.views import FilmNewsPageView

app_name='filmnews'

urlpatterns = [
    path('', FilmNewsPageView.as_view(), name='home'),
]