from django.urls import path

from film.views import HomePageView, FilmDetailPage, AllFilmListView, janrpage, YearPageView, CountryPageView, \
    KinoOlamPageView, SearchPageView, Mundarija, like_post, dislike_post, saved_post, RandomPage
from shared.views import DMCA, DMCAru, Feedback, Admin, AllUsers, ads_view, About, Foydalan, CreateWeb
from users.profile import Profile, EditProfile, PasswordChange
from django.conf.urls import handler404

app_name = 'film'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('film/<slug:slug>/', FilmDetailPage.as_view(), name='film-detail-page'),
    path('film/', AllFilmListView.as_view(), name='all-films'),
    #profile
    path('profile/', Profile.as_view(), name='profile'),
    path('profile/edit/', EditProfile.as_view(), name="profile-edit"),
    path('profile/change/password/', PasswordChange.as_view(), name="password-change"),
    #feedback
    path('feedback/', Feedback.as_view(), name="feedback"),
    #Admin
    path('admin/', Admin.as_view(), name="admin"),
    #allusers
    path('all-users/', AllUsers.as_view(), name="allusers"),
    #ADS -rekalam
    path('ads/', ads_view.as_view(), name="ads"),
    path('about/',About.as_view(), name="about"),
    path('foydalanish/',Foydalan.as_view(), name="foydalanish"),
    path('createweb/', CreateWeb.as_view(), name='create-web'),
    #janr
    path('janr/<str:janr_name>/', janrpage, name="film-janr-page"),
    #like
    path('film/<str:slug>/like/', like_post, name='like_post'),
    path('film/<str:slug>/dislike/', dislike_post, name='like_post'),
    #saved film
    path('film/<str:slug>/saved/', saved_post, name="saved_post"),
     #year
    path('year/<int:year>/', YearPageView.as_view(), name="year"),
    #country
    path('country/<str:country>/', CountryPageView.as_view(), name='country'),
    #kinoolam
    path('KinoOlam/<str:title>/', KinoOlamPageView.as_view(), name='kinoolam'),
    #Qidiruv
    path('search/', SearchPageView.as_view(), name='search'),
    #DMCA
    path('dmca/', DMCA.as_view(), name='dmca'),
    path('dmca/ru/', DMCAru.as_view(), name='dmcaru'),
    #zaxira
    path('kino/', AllFilmListView.as_view()),
    path('barchasi/', HomePageView.as_view()),
    path('all/', AllFilmListView.as_view()),
    path('all-films/', HomePageView.as_view()),
    path('films/', AllFilmListView.as_view()),
    path('kinolar/', AllFilmListView.as_view()),
    path('kinomakon/', HomePageView.as_view()),
    #MUNDARIJA
    path('film-mundarija/', Mundarija.as_view(), name='mundarija'),
    #random
    path('tasodifiy/', RandomPage.as_view(), name="random" ),

]
handler404 = 'film.views.page_not_found'