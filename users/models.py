import random
import uuid
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.db import models
#VALIDATORS
import re
from django.core import validators
from django.utils.deconstruct import deconstructible




#My user model
def validate_file_size(value):
    filesize = value.size

    if filesize > 716800:  # 0.7MB
        raise ValidationError("Fayl hajmi 0.7MB dan katta bo'lmasligi kerak!")


@deconstructible
class ASCIIUsernameValidator(validators.RegexValidator):
    regex = r"^[\w.@+-]+\Z"
    message = _(
        "Yaroqli username kiriting. Bu qiymat harflar va raqamlardan iborat bo'lishi mumkin!"
        "and uppercase A-Z letters, numbers, and @/./+/-/_ characters."
    )
    flags = re.ASCII


@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r"^[\w.@+-]+\Z"
    message = _(
        "Yaroqli username kiriting. Bu qiymat harflardan iborat bo'lishi mumkin, "
        "raqamlar, va @/./+/-/_ belgilari."
    )
    flags = 0
# END validaots

username_validator = UnicodeUsernameValidator()


class CustomUser(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=32,
        unique=True,
        help_text=_(
            "harf, raqam va @/./+/-/_. lardan foydalaning. 32ta belgidan oshmasin"
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("Bu username allaqachon mavjud"),
        },
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    picture = models.ImageField(upload_to="users/profile_pics/", help_text='Rasm hajmi 0.7mb dan oshmasligi kerak. Iloji borija kvadrat rasm yuklashga harakat qiling',
                                default='users/profile_pics/user-default-pic.png', null=True, blank=True,

                                validators=[FileExtensionValidator(message='iltimos faqat rasm yuklang va hajmi 0.7mb dan oshmasligi kerak',allowed_extensions=['jpg', 'jpeg', 'png', 'avif', 'bmp', 'webp','svg','heic','heif','tiff','tif','bmp', 'gif']),validate_file_size] )
    bio = models.TextField(max_length=256, null=True, blank=True)

    second_id = models.IntegerField(null=True, blank=True)

    @property
    def full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"


    def save(self, *args, **kwargs):
        if self.username:
            self.username = self.username.lower()
        if self.first_name:
            self.first_name = self.first_name.title()
        if self.first_name:
            self.last_name = self.last_name.title()
        if self.email:
            normalize_email = self.email.lower()
            self.email = normalize_email
        if not self.second_id:
            second_id = random.randint(10000, 99999)
            while CustomUser.objects.filter(second_id=second_id):
                second_id = random.randint(10000, 99999)
            self.second_id = second_id
        super().save(*args, **kwargs)


    #Name
    def __str__(self):
        if self.first_name:
            return f"{self.first_name.title()} {self.last_name.title()}"
        return self.username.title()