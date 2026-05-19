from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import FilmList
import include

urlpatterns = [
    path('', views.index, name='index'),
    path('api/films/', views.FilmList.as_view(), name='film-list'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)