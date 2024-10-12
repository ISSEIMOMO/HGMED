# example/urls.py
from django.urls import path

from dbbase.views import terminal


urlpatterns = [
    path('', terminal),
]