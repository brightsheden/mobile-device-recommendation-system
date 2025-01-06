from django.urls import path
from .views import home,recommendai


urlpatterns = [
    path('', home, name='home'),
    path('recommend',recommendai, name='recommend' )
]
