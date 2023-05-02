from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static

from decouple import config
from .settings.drf_yasg import urlpatterns

admin.site.site_header = "Административная панель"
admin.site.index_title = "Модели"

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("home/", include("src.tour.urls")),
    path("local/", include("django.conf.urls.i18n")),
    path("users/", include("src.users.urls")),
    path("profiles/", include("src.profiles.urls")),
    *urlpatterns,
]
if config("DEBUG"):
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
