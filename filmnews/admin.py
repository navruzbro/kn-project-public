from django.contrib import admin
from filmnews.models import FilmNewsModel

class FilmNewsAdmin(admin.ModelAdmin):
    search_fields = ['title','body']

admin.site.register(FilmNewsModel, FilmNewsAdmin)