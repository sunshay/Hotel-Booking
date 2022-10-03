from django.contrib import admin
from .models import Person, Room,Comment,Booking, Category, Blog



    
# Model admin person.
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name","birth_date","phone","email","type_user")


# Model Admin room and booking
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('title','price','size','capacity','bed','published','status','image')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('created','name','email')

# Model admin blog by category
class BlogAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, BlogAdmin)
admin.site.register(Blog, BlogAdmin)