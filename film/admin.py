import random

from django.contrib import admin

from film import models


class QismInline(admin.TabularInline):
    model = models.SerialParts
    extra = 3






class FilmAdmin(admin.ModelAdmin):
    inlines = [QismInline]
    #Avto yoziluvchi slug
    #sana
    date_hierarchy = "publish_time"
    '''
    list_display = ('title','title_2','title_addtext','type',

              'imdb_rating', 'year','hashtag', 'yosh_chegarasi', 'bio',

              'poster','poster_16_9','teaser','trailer',#tez kunda teaser yuklanmaydida havole berib ketiladi

               'sifat480p','sifat720p','sifat1080p','sifat360p','sifat2K','sifat4K',

              'country','country2','country3',

              'language','language_2',

              'janr','janr_2','janr_3','janr_4','janr_5','janr_6',

              'bio','director','actors',

              'kinoolam',

              'davomiy_soat', 'davomiy_minut',

              #COntrollerlari
              'tavsiya','carouselda_korsat','filmni_korsatmaslik',

              'publish_time',
                    )'''
    search_fields = ['title', 'title_2', 'title_addtext', ]
    list_filter = ['type', 'janr', 'year', 'country','publish_time']

    #Actions  --
    actions = ['carousel',"carousel_disable", 'tavsiya' ,'tavsiya_disable',"vaqtinchalik_ochirish","vaqtinchalik_ochirilganlarni_tiklash"]
    def carousel(self, request, queryset):
        queryset.update(carouselda_korsat = True)
    def carousel_disable(self, request, queryset):
         queryset.update(carouselda_korsat=False)
    def tavsiya(self, request, queryset):
        queryset.update(tavsiya = True)
    def tavsiya_disable(self, request, queryset):
        queryset.update(tavsiya = False)
    def vaqtinchalik_ochirish(self, request, queryset):
        queryset.update(active=False)
    def vaqtinchalik_ochirilganlarni_tiklash(self, request, queryset):
        queryset.update(active=True)



# film

admin.site.register(models.FilmModel, FilmAdmin)
admin.site.register(models.KinoOlamModel)
admin.site.register(models.TypeModel)
admin.site.register(models.YearModel)
admin.site.register(models.JanrModel)
admin.site.register(models.JanrModel2)
admin.site.register(models.JanrModel3)
admin.site.register(models.JanrModel4)
admin.site.register(models.JanrModel5)
admin.site.register(models.JanrModel6)
admin.site.register(models.CountryModel)
admin.site.register(models.CountryModel2)
admin.site.register(models.CountryModel3)
admin.site.register(models.LanguageModel)
admin.site.register(models.LanguageModel2)
admin.site.register(models.SerialParts)
