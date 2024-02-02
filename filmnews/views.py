from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View


from filmnews.models import FilmNewsModel


class FilmNewsPageView(View):

    def get(self, request):
        films = FilmNewsModel.objects.all().order_by('-publish_time')

        #pagination 12ta news
        paginator = Paginator(films, 12)
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        context = {
            'films':page_obj,
        }
        return render(request, 'filmnews/film-news.html', context)




