from filmnews.models import FilmNewsModel


def filmnews(request):
    films = FilmNewsModel.objects.all().order_by('-publish_time')[:6]

    context = {
        'filmnews':films
    }
    return context