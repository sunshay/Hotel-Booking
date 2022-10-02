from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Room

# Create your views here.



from .models import Room

class HomePageView(TemplateView):

    template_name = "hotel/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_rooms'] = Room.objects.all()[:5]
        return context

