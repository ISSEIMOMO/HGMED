# example/urls.py
from django.urls import path

from dbbase.views import excel, pes#, terminal


urlpatterns = [
    path('', pes),
    path('excel/<str:chm>', excel, name="excel"),
    path('pes/', pes, name="pes"),
    path('pes/<str:chm>', pes),
]