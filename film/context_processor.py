import random
from django.db.models import Q
from film.models import JanrModel, YearModel, CountryModel, KinoOlamModel, FilmModel


def base(request):
    films = list(FilmModel.objects.filter(mualliflik=False, active=True))
    '''Mana shu yerdan kino olam filmlari o'zgartiriladi'''
    film_olam = FilmModel.objects.filter(mualliflik=False, active=True, kinoolam=1).order_by('-imdb_rating')



    # Agar kamida 5 ta obyekt mavjud bo'lsa
    if len(films) >= 6:
        # Tasodifiy 5 ta obyekt tanlash
        random_films = random.sample(films, 6)
    else:
        # Agar 5 ta yoki undan kam film mavjud bo'lsa, hamma filmni olish
        random_films = films
    #unutmanglar tasodiflar tasodifan bo'lmaydi
    context = {
        'tasodifiy':random_films,
        'film_olam':film_olam,
    }
    return context
def janrlar(request):
    janrlar = JanrModel.objects.all()
    search_query = request.GET.get('q','')
    context = {
        'janrlar':janrlar,
        'search_query':search_query,
    }
    return context

def yillar(request):
    yillar = YearModel.objects.all().order_by('-year')
    context = {
        'yillar':yillar
    }
    return context
def davlatlar(request):
    davlatlar = CountryModel.objects.all()
    context = {
        'davlatlar':davlatlar
    }

    return context

def kinoolamdef(request):
    kinoolam = KinoOlamModel.objects.all()
    context = {
        'kinoolamdef':kinoolam,
    }

    return context

