# example/urls.py
from django.urls import path

from dbbase.views import terminal, excel


urlpatterns = [
    path('', terminal),
    path('excel/<str:chm>', excel),
]