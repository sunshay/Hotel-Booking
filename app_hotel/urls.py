from django.urls import path
from .views import HomePageView, RoomView, ContactView, AboutView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('room_detail/<pk>/', RoomView.as_view(), name='room_detail'),
    path('contact/', ContactView.as_view(), name='contact'),
    
]