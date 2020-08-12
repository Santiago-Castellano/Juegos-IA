from django.urls import path
from Common.views import index

urlpatterns = [
    path('', index,name='Common_index'),
]