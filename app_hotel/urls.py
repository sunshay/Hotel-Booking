from django.urls import path
from .views import HomePageView, RoomView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('post/<pk>/<slug:slug>', RoomView.as_view(), name='post'),
    
]