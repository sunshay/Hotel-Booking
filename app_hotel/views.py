from django.shortcuts import render
from .models import Room

# Create your views here.

def home(request, template_name="hotel/index.html"):
    context= {}
    messages = "Hello Hotel Booking"
    # object instance
    r1 = Room()
    r2 = Room()
    r3 = Room()
    
    # first object
    r1.name= "Premium King Room 1"
    r1.price= 100
    
    # second object
    r2.name= "Premium King Room 2"
    r2.price= 130
    
    # third object
    r3.name= "Premium King Room 3"
    r3.price= 140
    
    # list for all object
    list_room = [r1, r2, r3]
    

    
    
    context['messages'] = messages
    context['room_lists'] = list_room
    return render(request, template_name, context)
