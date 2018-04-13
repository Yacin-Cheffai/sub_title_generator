from django.urls import path
from . import views
app_name = 'generator'
urlpatterns = [
    path('', views.upload, name = 'upload'),
    path('syncmap.srt/', views.download, name = 'download')
]
