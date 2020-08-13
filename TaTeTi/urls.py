from django.urls import path
from TaTeTi.views import index, play_ai

urlpatterns = [
    path('', index,name='TaTeTi_index'),
    path('play_ai/', play_ai,name='TaTeTi_play_ai'),
]