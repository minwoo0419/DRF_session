from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name="music"
urlpatterns = [
    path('', views.album_list_create),
    path('<int:album_id>', views.album_detail_update_delete),
    path('<int:album_id>/track', views.track_list_create),
    path('<int:album_id>/track/<int:track_id>', views.track_detail_update_delete),
    path('tags', views.find_tag2),
    path('tags/<str:tag_name>', views.find_tag1),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
