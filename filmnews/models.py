from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

def validate_file_size(value):
    filesize = value.size

    if filesize > 716800:  # 0.7MB
        raise ValidationError("Fayl hajmi 0.7MB dan katta bo'lmasligi kerak!")

def validate_video_size(value):
    filesize = value.size

    if filesize > 12416800:  #5MB
        raise ValidationError("Fayl hajmi 12MB dan katta bo'lmasligi kerak!")

class FilmNewsModel(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='film-news/images',
                              default='film-news/images/filmnews.jpg',
                              null=True, blank=True,help_text="Rasm va Video 16:9 formatda bo'lishi kerak",
    validators = [FileExtensionValidator(message='iltimos faqat rasm yuklang va hajmi 0.7mb dan oshmasligi kerak',
                                         allowed_extensions=['jpg', 'jpeg', 'png', 'avif', 'bmp', 'webp', 'svg', 'heic',
                                                             'heif', 'tiff', 'tif', 'bmp', 'gif']), validate_file_size]
                              )

    video = models.FileField(upload_to='film-news/videos', null=True, blank=True,
                             validators=[FileExtensionValidator(
                                 message='iltimos faqat video yuklang va hajmi 12mb dan oshmasligi kerak'), validate_video_size]

                             )
    youtube = models.TextField(null=True, blank=True,max_length=300)
    body = models.TextField(max_length=400)
    publish_time = models.DateTimeField(default=timezone.now)
    create_time = models.DateTimeField(auto_now_add=True, blank=True)
    update_time = models.DateTimeField(auto_now=True, blank=True)


    def __str__(self):
        return self.title