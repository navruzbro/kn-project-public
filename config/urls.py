from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin-advanced/', admin.site.urls),
    path('', include('film.urls')),
    path('users/', include('users.urls')),
    path("news/", include("filmnews.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
