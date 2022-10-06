from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from .models import Room, Comment
from .form import CommentForm
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.


class HomePageView(TemplateView):

    template_name = "hotel/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_rooms'] = Room.objects.all()[:5]
        return context
    
class BlogView(TemplateView):
    
    template_name = "hotel/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_rooms'] = Room.objects.all()[:5]
        return context

class RoomView(DetailView):
    model = Room
    template_name = "hotel/room_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        slug = self.kwargs["slug"]

        form = CommentForm()
        post_room = get_object_or_404(Room, pk=pk, slug=slug)
        comments = post_room.comment_set.all()

        context['post_room'] = post_room
        context['comments'] = comments
        context['form'] = form
        return context
    # create a post for show one and to make a comment
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        post_room = Room.objects.filter(id=self.kwargs['pk'])[0]
        comments = post_room.comment_set.all()
        
        context['post'] = post_room
        context['comments'] = comments
        context['form'] = form

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']

            comment = Comment.objects.create(
                name=name, email=email, content=content, post=post_room
            )

            form = CommentForm()
            context['form'] = form
            return self.render_to_response(context=context)

        return self.render_to_response(context=context)