from django.urls import path
from .views import *

urlpatterns = [
    path("receive/", receive, name='receive'),
    path('send/', sender),
]