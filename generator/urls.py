from django.urls import path
from . import views
app_name = 'generator'
urlpatterns = [
    path('', views.upload, name = 'upload'),
    path('results.txt/', views.download, name = 'download')
]
