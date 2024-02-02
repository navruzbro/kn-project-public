import random

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

from film.models import FilmModel, JanrModel, JanrModel2, JanrModel6, JanrModel5, JanrModel3, JanrModel4, YearModel, \
    CountryModel, CountryModel2, CountryModel3, KinoOlamModel, FilmLike, FilmSaved
from users.models import CustomUser


# Create your views here.


class HomePageView(View):
    def get(self, request):
        order_by_config = request.GET.get('order_by', '')
        filter_config = request.GET.get('filter', '')
        # Type order
        order_by_type = request.GET.get('turi', '')
        default_order_by = 'publish_time'

        if order_by_type == 'kino':
            if filter_config == 'True':
                films = FilmModel.objects.filter(type=1, tavsiya=True, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')[:10]
            else:
                films = FilmModel.objects.filter(type=1, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')[:10]
        elif order_by_type == 'multfilm':
            if filter_config == 'True':
                films = FilmModel.objects.filter(type=2, tavsiya=True, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')[:10]
            else:
                films = FilmModel.objects.filter(type=2, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')[:10]
        elif order_by_type == 'serial':
            if filter_config == 'True':
                films = FilmModel.objects.filter(type=3, tavsiya=True, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')[:10]
            else:
                films = FilmModel.objects.filter(type=3, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')[:10]
        else:
            if filter_config == 'True':
                films = FilmModel.objects.filter(tavsiya=True, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')[:10]
            else:
                films = FilmModel.objects.filter(active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')[:10]

        carousel_film = FilmModel.objects.filter(carouselda_korsat=True, active=True).order_by("-publish_time")[:10]

        # buttonlarni active qilish va paginator uchun juda muhim sozlama
        if order_by_config == 'kinomakon_rating':
            active = 'kinomakon_rating'
        elif order_by_config == 'imdb_rating':
            active = 'imdb_rating'
        else:
            active = 'publish_time'

        # active_type turini aniqlash
        if order_by_type == 'kino':
            active_type = 'kino'
        elif order_by_type == 'multfilm':
            active_type = 'multfilm'
        elif order_by_type == 'serial':
            active_type = 'serial'
        else:
            active_type = 'all'


        #for hitcount

        context = {
            'films': films,
            'active': active,
            'active_type': active_type,

            # for carousel
            'carousel_film': carousel_film,

        }

        return render(request, 'index.html', context)


def page_not_found(request, exception):
    return render(request, '404.html', status=404)


class FilmDetailPage(View):
    def get(self, request, slug, *args, **kwargs):
        film = get_object_or_404(FilmModel, slug=slug)

        like_count = FilmLike.objects.filter(like=True, film=film).count()
        dislike_count = FilmLike.objects.filter(like=False, film=film).count()
        all_count = like_count - dislike_count
        if like_count + dislike_count != 0:
            likedis = like_count + dislike_count
            likdis = like_count / likedis
            kn_rat = likdis * 100
            film.kinomakon_rating = kn_rat
            film.save()
        if all_count > 0:
            alllike_count = f'+{all_count}'
        else:
            alllike_count = f'{all_count}'

        filmpartbormi = 'false'
        # FILM QISMLARI
        filmparts = FilmModel.objects.filter(title=film.title, active=True).order_by("-kinomakon_rating")
        if filmparts.count() > 1:
            filmpartbormi = 'true'
        # FILM KINOLAMI
        filmkinoolams = FilmModel.objects.filter(kinoolam=film.kinoolam, active=True).order_by("-imdb_rating")[:8]
        # FILM O'XSHASH
        filmaslikes = FilmModel.objects.filter(Q(janr=film.janr) | Q(janr_2=film.janr_2), active=True, type=film.type).order_by("-imdb_rating")[:8]

        #check saved
        savedd = "Saqlash"
        if request.user.is_authenticated:
            if request.user.saved.filter(saved=True, film=film):
                savedd="Saqlangan"



        context = {
            'film': film,
            # like and dislike context
            'likes_count': alllike_count,
            "savedd":savedd,
            # FILM plus section
            'filmparts': filmparts,
            'filmkinoolams': filmkinoolams,
            'filmaslike': filmaslikes,
            'filmpartbormi': filmpartbormi,
        }
        # hitcount logic
        hit_count = get_hitcount_model().objects.get_for_object(film)
        hits = hit_count.hits
        hitcontext = context['hitcount'] = {'pk': hit_count.pk}
        hit_count_response = HitCountMixin.hit_count(request, hit_count)

        if hit_count_response.hit_counted:
            hits = hits + 1
            hitcontext['hit_counted'] = hit_count_response.hit_counted
            hitcontext['hit_message'] = hit_count_response.hit_message
            hitcontext['total_hits'] = hits
        # END hitcount logic


        return render(request, 'film/film.html', context)



@csrf_exempt
def saved_post(request, slug):
    film = get_object_or_404(FilmModel, slug=slug)
    if request.method == 'POST':
        saqlash = "Saqlash"
        if request.user.is_authenticated:

            saved, created = FilmSaved.objects.get_or_create(user=request.user, film=film, saved=True)
            saqlash = "Film Saqlandi"
            if not created:
                saved.delete()
                saqlash = "Saqlash"

        return JsonResponse({'saqlash':saqlash })
    return JsonResponse({'error': 'Qandaydir bemani xatolik yuz berdi'}, status=405)
@csrf_exempt
def like_post(request, slug):
    film = get_object_or_404(FilmModel, slug=slug)
    if request.method == 'POST':
        if request.user.is_authenticated:
            like, created = FilmLike.objects.get_or_create(user=request.user, film=film, like=True)
            if not created:
                like.delete()

        like_count = FilmLike.objects.filter(like=True, film=film).count()
        dislike_count = FilmLike.objects.filter(like=False, film=film).count()
        all_count = like_count - dislike_count
        if like_count + dislike_count != 0:
            likedis = like_count + dislike_count
            likdis = like_count / likedis
            kn_rat = likdis * 100
            kn_rat = round(kn_rat, 1)
        if all_count > 0:
            likes_count = f'+{all_count}'
        else:
            likes_count = f'{all_count}'
        return JsonResponse({'likes_count': likes_count, 'kn_rat': kn_rat})
    return JsonResponse({'error': 'Qandaydir bemani xatolik yuz berdi'}, status=405)


@csrf_exempt
def dislike_post(request, slug):
    film = get_object_or_404(FilmModel, slug=slug)
    if request.method == 'POST':
        if request.user.is_authenticated:
            dislike, created = FilmLike.objects.get_or_create(user=request.user, film=film, like=False)
            if not created:
                dislike.delete()

        like_count = FilmLike.objects.filter(like=True, film=film).count()
        dislike_count = FilmLike.objects.filter(like=False, film=film).count()
        all_count = like_count - dislike_count
        if like_count + dislike_count != 0:
            likedis = like_count + dislike_count
            likdis = like_count / likedis
            kn_rat = likdis * 100
            kn_rat = round(kn_rat, 1)
        if all_count > 0:
            likes_count = f'+{all_count}'
        else:
            likes_count = f'{all_count}'
        return JsonResponse({'likes_count': likes_count, 'kn_rat': kn_rat})
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# all films
class AllFilmListView(View):
    def get(self, request):
        order_by_config = request.GET.get('order_by', '')
        filter_config = request.GET.get('filter', '')

        # Agar order_by_config bo'sh bo'lsa, 'publish_time' ni o'zimizni tanlagan default qiymat sifatida ishlatamiz
        default_order_by = 'publish_time'

        # Type order
        order_by_type = request.GET.get('turi', '')

        if order_by_type == 'serial':
            if filter_config == 'True':
                films = FilmModel.objects.filter(type=3, tavsiya=True, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
            else:
                films = FilmModel.objects.filter(type=3, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
        elif order_by_type == 'multfilm':
            if filter_config == 'True':
                films = FilmModel.objects.filter(type=2, tavsiya=True, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
            else:
                films = FilmModel.objects.filter(type=2, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
        elif order_by_type == 'kino':
            if filter_config == 'True':
                films = FilmModel.objects.filter(type=1, tavsiya=True, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
            else:
                films = FilmModel.objects.filter(type=1, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
        else:
            if filter_config == 'True':
                films = FilmModel.objects.filter(tavsiya=True, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
            else:
                films = FilmModel.objects.filter(active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')

        paginator = Paginator(films, 8)
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        # buttonlarni active qilish va paginator uchun juda muhim sozlama
        if order_by_config == 'kinomakon_rating':
            active = 'kinomakon_rating'
        elif order_by_config == 'imdb_rating':
            active = 'imdb_rating'
        else:
            active = 'publish_time'

        # typeni aniqlash uchun
        if order_by_type == 'kino':
            active_type = 'kino'
        elif order_by_type == 'multfilm':
            active_type = 'multfilm'
        elif order_by_type == 'serial':
            active_type = 'serial'
        else:
            active_type = 'all'

        context = {
            'allfilms': page_obj,
            'active': active,
            'active_type': active_type,
        }
        return render(request, "film/all-film.html", context)


class YearPageView(View):
    def get(self, request, year):
        year = get_object_or_404(YearModel, year=year)
        # FIlm configs
        order_by_config = request.GET.get('order_by', '')
        filter_config = request.GET.get('filter', '')

        # Agar order_by_config bo'sh bo'lsa, 'publish_time' ni o'zimizni tanlagan default qiymat sifatida ishlatamiz
        default_order_by = 'publish_time'

        # Type order
        order_by_type = request.GET.get('turi', '')

        if order_by_type == 'serial':
            if filter_config == 'True':
                films = FilmModel.objects.filter(year=year, type=3, tavsiya=True, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
            else:
                films = FilmModel.objects.filter(year=year, type=3, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
        elif order_by_type == 'multfilm':
            if filter_config == 'True':
                films = FilmModel.objects.filter(year=year, type=2, tavsiya=True, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
            else:
                films = FilmModel.objects.filter(year=year, type=2, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
        elif order_by_type == 'kino':
            if filter_config == 'True':
                films = FilmModel.objects.filter(year=year, type=1, tavsiya=True, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
            else:
                films = FilmModel.objects.filter(year=year, type=1, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
        else:
            if filter_config == 'True':
                films = FilmModel.objects.filter(year=year, tavsiya=True, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
            else:
                films = FilmModel.objects.filter(year=year, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')

        paginator = Paginator(films, 8)
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        # buttonlarni active qilish va paginator uchun juda muhim sozlama
        if order_by_config == 'kinomakon_rating':
            active = 'kinomakon_rating'
        elif order_by_config == 'imdb_rating':
            active = 'imdb_rating'
        else:
            active = 'publish_time'

        # endfilmconfigs
        # typeni aniqlash uchun
        if order_by_type == 'kino':
            active_type = 'kino'
        elif order_by_type == 'multfilm':
            active_type = 'multfilm'
        elif order_by_type == 'serial':
            active_type = 'serial'
        else:
            active_type = 'all'
        context = {
            'year': year,
            'allfilms': page_obj,
            'active': active,
            'active_type': active_type
        }
        return render(request, 'film/year.html', context)


class CountryPageView(View):
    def get(self, request, country):

        country_2 = get_object_or_404(CountryModel2, country=country)
        country_3 = get_object_or_404(CountryModel3, country=country)
        country = get_object_or_404(CountryModel, country=country)

        # FIlm configs
        order_by_config = request.GET.get('order_by', '')
        filter_config = request.GET.get('filter', '')

        # Agar order_by_config bo'sh bo'lsa, 'publish_time' ni o'zimizni tanlagan default qiymat sifatida ishlatamiz
        default_order_by = 'publish_time'

        # Type order
        order_by_type = request.GET.get('turi', '')

        filter_country = Q(country=country) | Q(country2=country_2) | Q(country3=country_3)

        if order_by_type == 'serial':
            if filter_config == 'True':
                films = FilmModel.objects.filter(filter_country, type=3, tavsiya=True, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
            else:
                films = FilmModel.objects.filter(filter_country, type=3, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
        elif order_by_type == 'multfilm':
            if filter_config == 'True':
                films = FilmModel.objects.filter(filter_country, type=2, tavsiya=True, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
            else:
                films = FilmModel.objects.filter(filter_country, type=2, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
        elif order_by_type == 'kino':
            if filter_config == 'True':
                films = FilmModel.objects.filter(filter_country, type=1, tavsiya=True, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
            else:
                films = FilmModel.objects.filter(filter_country, type=1, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
        else:
            if filter_config == 'True':
                films = FilmModel.objects.filter(filter_country, tavsiya=True, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
            else:
                films = FilmModel.objects.filter(filter_country, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')

        paginator = Paginator(films, 8)
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        # buttonlarni active qilish va paginator uchun juda muhim sozlama
        if order_by_config == 'kinomakon_rating':
            active = 'kinomakon_rating'
        elif order_by_config == 'imdb_rating':
            active = 'imdb_rating'
        else:
            active = 'publish_time'

        # typeni aniqlash uchun
        if order_by_type == 'kino':
            active_type = 'kino'
        elif order_by_type == 'multfilm':
            active_type = 'multfilm'
        elif order_by_type == 'serial':
            active_type = 'serial'
        else:
            active_type = 'all'
        context = {
            'allfilms': page_obj,
            'country': country,
            'active': active,
            'active_type': active_type,
        }
        return render(request, 'film/country.html', context)


def janrpage(request, janr_name, *args, **kwargs):
    janr_6 = get_object_or_404(JanrModel6, janr=janr_name)
    janr_5 = get_object_or_404(JanrModel5, janr=janr_name)
    janr_4 = get_object_or_404(JanrModel4, janr=janr_name)
    janr_3 = get_object_or_404(JanrModel3, janr=janr_name)
    janr_2 = get_object_or_404(JanrModel2, janr=janr_name)
    janr = get_object_or_404(JanrModel, janr=janr_name)

    # FIlm configs
    order_by_config = request.GET.get('order_by', '')
    filter_config = request.GET.get('filter', '')

    # Agar order_by_config bo'sh bo'lsa, 'publish_time' ni o'zimizni tanlagan default qiymat sifatida ishlatamiz
    default_order_by = 'publish_time'

    # Type order
    order_by_type = request.GET.get('turi', '')

    filter_janr = Q(janr=janr) | Q(janr_2=janr_2) | Q(janr_3=janr_3) | Q(janr_4=janr_4) | Q(janr_5=janr_5) | Q(
        janr_6=janr_6)

    if order_by_type == 'serial':
        if filter_config == 'True':
            films = FilmModel.objects.filter(filter_janr, type=3, tavsiya=True, active=True).order_by(
                f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
        else:
            films = FilmModel.objects.filter(filter_janr, type=3, active=True).order_by(
                f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
    elif order_by_type == 'multfilm':
        if filter_config == 'True':
            films = FilmModel.objects.filter(filter_janr, type=2, tavsiya=True, active=True).order_by(
                f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
        else:
            films = FilmModel.objects.filter(filter_janr, type=2, active=True).order_by(
                f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
    elif order_by_type == 'kino':
        if filter_config == 'True':
            films = FilmModel.objects.filter(filter_janr, type=1, tavsiya=True, active=True).order_by(
                f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
        else:
            films = FilmModel.objects.filter(filter_janr, type=1, active=True).order_by(
                f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
    else:
        if filter_config == 'True':
            films = FilmModel.objects.filter(filter_janr, tavsiya=True, active=True).order_by(
                f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
        else:
            films = FilmModel.objects.filter(filter_janr, active=True).order_by(
                f'-{order_by_config}' if order_by_config else f'-{default_order_by}')

    paginator = Paginator(films, 8)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)

    # buttonlarni active qilish va paginator uchun juda muhim sozlama
    if order_by_config == 'kinomakon_rating':
        active = 'kinomakon_rating'
    elif order_by_config == 'imdb_rating':
        active = 'imdb_rating'
    else:
        active = 'publish_time'

    # typeni aniqlash uchun
    if order_by_type == 'kino':
        active_type = 'kino'
    elif order_by_type == 'multfilm':
        active_type = 'multfilm'
    elif order_by_type == 'serial':
        active_type = 'serial'
    else:
        active_type = 'all'
    context = {
        'janr': janr,
        'allfilms': page_obj,
        'active': active,
        'active_type': active_type,

    }
    return render(request, 'film/janr.html', context)


class KinoOlamPageView(View):
    def get(self, request, title):
        kinoolam = get_object_or_404(KinoOlamModel, title=title)
        # FIlm configs
        order_by_config = request.GET.get('order_by', '')
        filter_config = request.GET.get('filter', '')

        # Agar order_by_config bo'sh bo'lsa, 'publish_time' ni o'zimizni tanlagan default qiymat sifatida ishlatamiz
        default_order_by = 'publish_time'

        # Type order
        order_by_type = request.GET.get('turi', '')

        if order_by_type == 'serial':
            if filter_config == 'True':
                films = FilmModel.objects.filter(kinoolam=kinoolam, type=3, tavsiya=True, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
            else:
                films = FilmModel.objects.filter(kinoolam=kinoolam, type=3, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
        elif order_by_type == 'multfilm':
            if filter_config == 'True':
                films = FilmModel.objects.filter(kinoolam=kinoolam, type=2, tavsiya=True, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
            else:
                films = FilmModel.objects.filter(kinoolam=kinoolam, type=2, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
        elif order_by_type == 'kino':
            if filter_config == 'True':
                films = FilmModel.objects.filter(kinoolam=kinoolam, type=1, tavsiya=True, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
            else:
                films = FilmModel.objects.filter(kinoolam=kinoolam, type=1, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
        else:
            if filter_config == 'True':
                films = FilmModel.objects.filter(kinoolam=kinoolam, tavsiya=True, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
            else:
                films = FilmModel.objects.filter(kinoolam=kinoolam, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')

        paginator = Paginator(films, 8)
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        # buttonlarni active qilish va paginator uchun juda muhim sozlama
        if order_by_config == 'kinomakon_rating':
            active = 'kinomakon_rating'
        elif order_by_config == 'imdb_rating':
            active = 'imdb_rating'
        else:
            active = 'publish_time'

        # endfilmconfigs
        # typeni aniqlash uchun
        if order_by_type == 'kino':
            active_type = 'kino'
        elif order_by_type == 'multfilm':
            active_type = 'multfilm'
        elif order_by_type == 'serial':
            active_type = 'serial'
        else:
            active_type = 'all'

        context = {
            'kinoolam': kinoolam,
            'allfilms': page_obj,
            'active': active,
            'active_type': active_type,
        }

        return render(request, 'film/kinoolam.html', context)


# Search -- Qidiruv

class SearchPageView(View):
    def get(self, request):
        films = FilmModel.objects.all()
        search_query = request.GET.get('q', '')
        if search_query:
            films = films.filter(
                Q(full_title__icontains=search_query) |
                Q(title_2__icontains=search_query) |
                Q(title_addtext__icontains=search_query) |
                Q(kinoolam__title__icontains=search_query) |
                Q(hashtag__icontains=search_query) |
                Q(director__icontains=search_query) |
                Q(actors__icontains=search_query) |
                Q(janr__janr__icontains=search_query) |
                Q(janr_2__janr__icontains=search_query) |
                Q(janr_3__janr__icontains=search_query) |
                Q(janr_4__janr__icontains=search_query) |
                Q(janr_5__janr__icontains=search_query) |
                Q(janr_6__janr__icontains=search_query) |
                Q(country__country__icontains=search_query) |
                Q(film_code__icontains=search_query), active=True
            )

        paginator = Paginator(films, 12)
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        context = {
            'allfilms': page_obj,
        }

        return render(request, 'film/search.html', context)


class Mundarija(View):
    def get(self, request):
        order_by_config = request.GET.get('order_by', '')
        filter_config = request.GET.get('filter', '')

        default_order_by = 'publish_time'

        # Type order
        order_by_type = request.GET.get('turi', '')

        if order_by_type == 'serial':
            if filter_config == 'True':
                films = FilmModel.objects.filter(type=3, tavsiya=True, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
            else:
                films = FilmModel.objects.filter(type=3, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
        elif order_by_type == 'multfilm':
            if filter_config == 'True':
                films = FilmModel.objects.filter(type=2, tavsiya=True, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
            else:
                films = FilmModel.objects.filter(type=2, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
        elif order_by_type == 'kino':
            if filter_config == 'True':
                films = FilmModel.objects.filter(type=1, tavsiya=True, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
            else:
                films = FilmModel.objects.filter(type=1, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
        else:
            if filter_config == 'True':
                films = FilmModel.objects.filter(tavsiya=True, active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')
            else:
                films = FilmModel.objects.filter(active=True).order_by(
                    f'-{order_by_config}' if order_by_config else f'-{default_order_by}')

        # buttonlarni active qilish va paginator uchun juda muhim sozlama
        if order_by_config == 'kinomakon_rating':
            active = 'kinomakon_rating'
        elif order_by_config == 'imdb_rating':
            active = 'imdb_rating'
        else:
            active = 'publish_time'

        # typeni aniqlash uchun
        if order_by_type == 'kino':
            active_type = 'kino'
        elif order_by_type == 'multfilm':
            active_type = 'multfilm'
        elif order_by_type == 'serial':
            active_type = 'serial'
        else:
            active_type = 'all'

        context = {

            'films': films,
            'active': active,
            'active_type': active_type,

        }
        return render(request, 'film/mundarija.html', context)


class RandomPage(View):
    def get(self, request):
        # Type order
        order_by_type = request.GET.get('turi', '')

        if order_by_type == 'serial':
            films = list(FilmModel.objects.filter(type=3, tavsiya=True, active=True))
            active_type = 'serial'
        elif order_by_type == 'multfilm':
            films = list(FilmModel.objects.filter(type=2, tavsiya=True, active=True))
            active_type = 'multfilm'
        elif order_by_type == 'kino':
            films = list(FilmModel.objects.filter(type=1, tavsiya=True, active=True))
            active_type = 'kino'
        else:
            films = list(FilmModel.objects.filter( tavsiya=True, active=True))
            active_type = 'all'

        # Agar kamida 5 ta obyekt mavjud bo'lsa
        if len(films) >= 1:
            # Tasodifiy 5 ta obyekt tanlash
            random_films = random.sample(films, 8)
        else:
            # Agar 5 ta yoki undan kam film mavjud bo'lsa, hamma filmni olish
            random_films = films

        refresh = random.randint(1, 13)
        # unutmanglar tasodiflar tasodifan bo'lmaydi
        context = {
            'randomfilms': random_films,
            'active_type': active_type,
            "refresh":refresh,
        }

        return render(request, 'film/random-film.html', context)

#version = 1.0
