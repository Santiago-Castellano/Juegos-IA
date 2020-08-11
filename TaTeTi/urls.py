from django.urls import path
from TaTeTi.views import index

urlpatterns = [
    path('', index),
]