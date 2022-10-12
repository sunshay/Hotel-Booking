from django.urls import path
from .views import (HomePageView, RoomView, 
                    ContactView, AboutView, RoomAllView, BlogAllView)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('rooms/', RoomAllView.as_view(), name='rooms'),
    path('blogs/', BlogAllView.as_view(), name='blogs'),
    path('room_detail/<pk>/', RoomView.as_view(), name='room_detail'),
    path('contact/', ContactView.as_view(), name='contact'),
    
]