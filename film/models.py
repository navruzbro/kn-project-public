import random
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from users.models import CustomUser


class JanrModel(models.Model):
    janr = models.CharField(max_length=100)
    def janr_url(self):
        url = reverse('film:film-janr-page', args=[self.janr])
        return url


    def __str__(self):
        return self.janr
class JanrModel2(models.Model):
    janr = models.CharField(max_length=100)


    def janr_url(self):
        url = reverse('film:film-janr-page', args=[self.janr])
        return url


    def __str__(self):
        return self.janr
class JanrModel3(models.Model):
    janr = models.CharField(max_length=100)


    def janr_url(self):
        url = reverse('film:film-janr-page', args=[self.janr])
        return url


    def __str__(self):
        return self.janr
class JanrModel4(models.Model):
    janr = models.CharField(max_length=100)


    def janr_url(self):

        url = reverse('film:film-janr-page', args=[self.janr])
        return url

    def __str__(self):
        return self.janr
class JanrModel5(models.Model):

    janr = models.CharField(max_length=100)


    def janr_url(self):
        url = reverse('film:film-janr-page', args=[self.janr])
        return url


    def __str__(self):
        return self.janr
class JanrModel6(models.Model):


    janr = models.CharField(max_length=100)


    def janr_url(self):
        url = reverse('film:film-janr-page', args=[self.janr])
        return url


    def __str__(self):
        return self.janr
class LanguageModel(models.Model):
    language = models.CharField(max_length=20)


    def __str__(self):
        return self.language
class LanguageModel2(models.Model):
    language = models.CharField(max_length=20)


    def __str__(self):
        return self.language
class CountryModel(models.Model):
    country = models.CharField(max_length=20)


    def __str__(self):
        return self.country


    def country_url(self):
        url = reverse('film:country', args=[self.country])
        return url
class CountryModel2(models.Model):
    country = models.CharField(max_length=20)


    def __str__(self):
        return self.country


    def country_url(self):
        url = reverse('film:country', args=[self.country])
        return url


class CountryModel3(models.Model):
    country = models.CharField(max_length=20)

    def __str__(self):
        return self.country

    def country_url(self):
        url = reverse('film:country', args=[self.country])
        return url

class TypeModel(models.Model):
    type = models.CharField(max_length=20)
    def __str__(self):
        return self.type


class KinoOlamModel(models.Model):
    title = models.CharField(max_length=100)
    title_2 = models.CharField(max_length=100,null=True, blank=True)
    bio = models.TextField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return self.title

    def kinoolam_url(self):
        url = reverse('film:kinoolam', args=[self.title])
        return url

class YearModel(models.Model):
    year = models.IntegerField(
        validators=[MinValueValidator(1940), MaxValueValidator(2100)]
    )
    def __str__(self):
        stryear = str(self.year)
        return stryear
    def year_url(self):
        url = reverse('film:year', args=[self.year])
        return url


def validate_video_size(value):
    filesize = value.size

    if filesize > 15516800:  # 15MB
        raise ValidationError("Fayl hajmi 15MB dan katta bo'lmasligi kerak!")

def validate_file_size(value):
    filesize = value.size

    if filesize > 716800:  # 0.7MB
        raise ValidationError("Fayl hajmi 0.7MB dan katta bo'lmasligi kerak!")


class FilmModel(models.Model):
    title = models.CharField(max_length=100 )
    title_2 = models.CharField(max_length=100, null=True, blank=True)
    title_addtext = models.CharField(max_length=200, null=True, blank=True)

    slug = models.SlugField(max_length=200,null=True,  blank=True, help_text="Bunga hech narsa yozma!!!!")
    year = models.ForeignKey(YearModel, on_delete=models.SET_NULL, null=True)
    poster = models.ImageField(upload_to="films/posters/", help_text="To'ldirish majburiy va Rasm hajmi 0.7mb dan baland bo'lmasligi shart!",
    validators = [FileExtensionValidator(message='iltimos faqat rasm yuklang va hajmi 0.7mb dan oshmasligi kerak',
                                         allowed_extensions=['jpg', 'jpeg', 'png', 'avif', 'bmp', 'webp', 'svg', 'heic',
                                                             'heif', 'tiff', 'tif', 'bmp', 'gif']), validate_file_size]
                               )
    poster_16_9 = models.ImageField(upload_to="films/posters_16_9", null=True, blank=True,help_text="Rasm hajmi 0.7mb dan baland bo'lmasligi shart!",
                                    validators=[validate_file_size]
                                    )
    # teaser
    teaser = models.FileField(upload_to='videos/film_teasers/', null=True, blank=True,
                              validators= [validate_video_size], help_text="Video hajmi 15 megabaytdan katta bo'lamsligi shart")
    trailer = models.CharField(max_length=500, null=True, blank=True,
                               help_text="YouTube html kod kiritiladi(notebook kerak) -- Agar teaser kiritsangiz, trailer kiritish shart emas")
    country = models.ForeignKey(CountryModel, on_delete=models.SET_NULL, null=True)
    country2 = models.ForeignKey(CountryModel2, on_delete=models.SET_NULL, null=True, blank=True)
    country3 = models.ForeignKey(CountryModel3, on_delete=models.SET_NULL, null=True, blank=True)
    language = models.ForeignKey(LanguageModel, on_delete=models.SET_NULL, null=True, )
    language_2 = models.ForeignKey(LanguageModel2, on_delete=models.SET_NULL, null=True, blank=True)

    sifat360p = models.TextField(max_length=1000, null=True, blank=True, help_text='Agar serial joylaseyz serial deb nomlangan inputlarni to\'ldiring')
    sifat480p = models.TextField(max_length=1000, null=True, blank=True)
    sifat720p = models.TextField(max_length=1000, null=True, blank=True)
    sifat1080p = models.TextField(max_length=1000, null=True, blank=True)
    sifat2K = models.TextField(max_length=1000, null=True, blank=True)
    sifat4K = models.TextField(max_length=1000, null=True, blank=True)

    janr = models.ForeignKey(JanrModel, on_delete=models.SET_NULL, null=True, related_name='films')
    janr_2 = models.ForeignKey(JanrModel2, on_delete=models.SET_NULL, null=True, blank=True)
    janr_3 = models.ForeignKey(JanrModel3, on_delete=models.SET_NULL, null=True, blank=True)
    janr_4 = models.ForeignKey(JanrModel4, on_delete=models.SET_NULL, null=True, blank=True)
    janr_5 = models.ForeignKey(JanrModel5, on_delete=models.SET_NULL, null=True, blank=True)
    janr_6 = models.ForeignKey(JanrModel6, on_delete=models.SET_NULL, null=True, blank=True)

    bio = models.TextField(max_length=3000, null=True, blank=True)
    actors = models.CharField(max_length=1000, null=True, blank=True)
    director = models.CharField(max_length=500, null=True, blank=True)
    yosh_chegarasi = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(30)], null=True, default=16 )
    kinomakon_rating = models.FloatField(null=True, default=0.0)
    imdb_rating = models.FloatField(null=True, default=0.0)
    hashtag = models.CharField(max_length=500, null=True, blank=True)
    davomiy_soat = models.CharField(max_length=4, null=True, blank=True)
    davomiy_minut = models.CharField(max_length=3, null=True, blank=True)
    kinoolam = models.ForeignKey(KinoOlamModel, on_delete=models.SET_NULL, null=True, blank=True)
    publish_time = models.DateTimeField(default=timezone.now)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    type = models.ForeignKey(TypeModel, on_delete=models.SET_NULL, null=True)
    full_title = models.CharField(max_length=200, null=True, blank=True, help_text="Hech narsa yozishingiz shart emas")
    carouselda_korsat = models.BooleanField(null=True, blank=True, default=False)
    tavsiya = models.BooleanField(null=True, blank=True, default=False)
    film_code = models.CharField( max_length=20, null=True, blank=True)
    mualliflik = models.BooleanField(default=False, help_text = "Film mualliflik huquqi buzilsa shu orqali o'chirib qo'yiladi...!")
    active = models.BooleanField(default=True, help_text="vaqtinchalik o'chirib qo'yish mumkin ....")

    def random_number(self):
        random_num = str(random.randint(1000, 9999))
        return random_num

    def save(self, *args, **kwargs):
        if not self.slug:
            if self.title_2:
                self.slug = slugify(f"{self.title} {self.title_2}-{random.randint(0,1000)}")
            else:
                self.slug = slugify(f"{self.title}-{random.randint(0, 1000)}")
        if not self.full_title:
            self.full_title = f"{self.title} {self.title_2}"
        if not self.film_code:
            film_code = f'{random.randint(1000, 9999)}'
            while FilmModel.objects.filter(film_code=film_code):
                film_code = f'{random.randint(10, 99) + random.randint(10, 99)}'
            self.film_code = film_code
        if self.kinomakon_rating:
            self.kinomakon_rating = round(self.kinomakon_rating, 1)
            self.imdb_rating = round(self.imdb_rating, 1)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} {self.title_2}"


    def get_absolute_url(self):
        return reverse("film:film-detail-page", args=[self.slug])

    def janr_url(self):
        url = reverse('film:film-janr-page', args=[self.janr.janr])
        return url

    def year_url(self):
        url = reverse('film:year', args=[self.year])
        return url

    def country_url(self):
        url = reverse('film:country', args=[self.country])
        return url

    def kinoolam_url(self):
        url = reverse('film:kinoolam', args=[self.kinoolam])
        return url

    def serial_part(self):
        return self.serial_qism.all()



class SerialParts(models.Model):
    title = models.CharField(max_length=50)
    href = models.CharField(max_length=333)
    filmqism = models.ForeignKey(FilmModel, on_delete=models.CASCADE, related_name="serialqism")

    def __str__(self):
        return f"{self.title} {self.filmqism.title} {self.filmqism.title_2}"



class FilmLike(models.Model):
    film = models.ForeignKey(FilmModel, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='like')
    like = models.BooleanField(null=True, blank=True)
    publish_time = models.DateTimeField(default=timezone.now)

class FilmSaved(models.Model):
    film = models.ForeignKey(FilmModel, on_delete=models.CASCADE, related_name='saved')
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='saved')
    #saved
    saved = models.BooleanField(default=False)
    publish_time = models.DateTimeField(default=timezone.now)



