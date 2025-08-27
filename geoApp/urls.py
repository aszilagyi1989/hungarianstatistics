from django.urls import path
from django.contrib.auth import views as auth_views
""" from . import views """
from geoApp.views import geopandas

urlpatterns = [
   path('home/', geopandas, name='geopandas'),   # Home page (requires login)
]