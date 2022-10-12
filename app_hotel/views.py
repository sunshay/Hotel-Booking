import email
from django.shortcuts import render,redirect
from django.http import HttpResponse 
from django.views.generic import TemplateView, DetailView,View, CreateView
from .models import Contact, Room, Comment,Reservation, User
from .form import CommentForm, ContactForm
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.contrib import messages
import datetime

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
    template_name = "hotel/room-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        #slug = self.kwargs["slug"]

        form = CommentForm()
        post_room = get_object_or_404(Room, pk=pk)
        comments = post_room.comment_set.all()
        reservation = Reservation.objects.all()

        context['post_room'] = post_room
        context['comments'] = comments
        context['form'] = form
        context['reservation'] = reservation
        return context
    # create a post for show one and to make a comment
    def post(self, request, *args, **kwargs):
        if request.method =="POST":
            form = CommentForm(request.POST)
            self.object = self.get_object()
            context = super().get_context_data(**kwargs)

            room_id = Room.objects.filter(id=self.kwargs['pk'])[0]
            comments = room_id.comment_set.all()
            
            context['post'] = room_id
            context['comments'] = comments
            context['form'] = form

            if form.is_valid():
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                content = form.cleaned_data['content']

                comment = Comment.objects.create(
                    name=name, email=email, content=content, room_blog=room_id
                )
                comment.save()
                messages.success(request,"Your comment Successfull")
                form = CommentForm()
                
                # user client 
                # name_user = request.POST['name_user']
                # email_user = request.POST['email_user']
                # phone_number = request.POST['phone_number']
                # user = User()
                # # user = User.objects.create(
                # #     username=name_user,phone_number=phone_number,email=email_user
                # # )
                # user.username = name_user
                # user.phone_number = phone_number
                # user.email = email_user
                # user.save()
                
                # reservation function
            
                room = Room.objects.all().get(id=room_id)
                #for finding the reserved rooms on this time period for excluding from the query set
                for each_reservation in Reservation.objects.all().filter(room = room_id):
                    if str(each_reservation.check_in) < str(request.POST['check_in']) and str(each_reservation.check_out) < str(request.POST['check_out']):
                        pass
                    elif str(each_reservation.check_in) > str(request.POST['check_in']) and str(each_reservation.check_out) > str(request.POST['check_out']):
                        pass
                    else:
                        messages.warning(request,"Sorry This Room is unavailable for Booking")
                        return redirect("homepage")
                current_user = request.user
                total_person = int( request.POST['number_guest'])
                booking_id = str(room_id) + str(datetime.datetime.now())

                reservation = Reservation()
                room_object = Room.objects.all().get(id=room_id)
                room_object.status = '2'
                
                user_object = User.objects.all().get(username=current_user)

                reservation.user = user_object
                reservation.room = room_object
                reservation.number_guest = total_person
                reservation.check_in = request.POST['check_in']
                reservation.check_out = request.POST['check_out']

                reservation.save()

                messages.success(request,"Congratulations! Booking Successfull")
                context['form'] = form
                return self.render_to_response(context=context)

            return self.render_to_response(context=context)
    
# class ReservationView(View):
    
#     def post(self, request, *args, **kwargs):
    
#         if request.method =="POST":

#             room_id = request.POST['room_id']
            
#             room = Room.objects.all().get(id=room_id)
#             #for finding the reserved rooms on this time period for excluding from the query set
#             for each_reservation in Reservation.objects.all().filter(room = room):
#                 if str(each_reservation.check_in) < str(request.POST['check_in']) and str(each_reservation.check_out) < str(request.POST['check_out']):
#                     pass
#                 elif str(each_reservation.check_in) > str(request.POST['check_in']) and str(each_reservation.check_out) > str(request.POST['check_out']):
#                     pass
#                 else:
#                     messages.warning(request,"Sorry This Room is unavailable for Booking")
#                     return redirect("homepage")
                
#             current_user = request.user
#             total_person = int( request.POST['person'])
#             booking_id = str(room_id) + str(datetime.datetime.now())

#             reservation = Reservation()
#             room_object = Room.objects.all().get(id=room_id)
#             room_object.status = '2'
            
#             user_object = Person.objects.all().get(username=current_user)

#             reservation.guest = user_object
#             reservation.room = room_object
#             person = total_person
#             reservation.check_in = request.POST['check_in']
#             reservation.check_out = request.POST['check_out']

#             reservation.save()

#             messages.success(request,"Congratulations! Booking Successfull")

#             return redirect("homepage")
#         else:
#             return HttpResponse('Access Denied')
    

class ContactView(View):
    model = Contact
    #template_name = "hotel/contact.html"
    success_msg = 'Contact created.'
    
    def get(self, request, *args, **kwargs):
        context = {}
        context['form']= ContactForm()
        return render(request, "hotel/contact.html", context)
    
     # create a post for show one and to make a comment
    def post(self, request, *args, **kwargs):
        form =  ContactForm(request.POST)
        context = {}
        
        context['form'] = form

        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            contact = Contact.objects.create(
               name=name,phone=phone, subject=subject, email=email, message=message,)
            contact.save()
            messages.success(request,"Your message Successfull")
            
            
            
            form = ContactForm()
            context['form'] = form
            #return render(request, "hotel/contact.html", context=context)
        

        return render(request, "hotel/contact.html", context=context)
    


    
    