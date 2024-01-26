from django.urls import path
from .views import MyChatBot

urlpatterns = [
    path('get-response/', MyChatBot.as_view(), name='get_response'),
]
