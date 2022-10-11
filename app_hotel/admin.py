from django.contrib import admin
from .models import Contact, Person, Room,Comment,Booking, Category, Blog
from django.utils.html import format_html

# change Django administration text Login, The listview page and The HTML title tag 
admin.site.site_header = "Hotel Booking"
admin.site.site_title = "Hotel Booking Admin Penal"
admin.site.index_title = "Welcome to Hotel Booking"
    
# Model admin person.
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name","birth_date","phone","email","type_user")


# Model Admin room and booking
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" width="100" height="50" />'.format(obj.image.url))

    image_tag.short_description = 'Image'
    list_display = ('title','price','size','capacity','bed','published','status','image_tag')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('created','name','email')

# Model admin blog by category
class BlogAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, BlogAdmin)
admin.site.register(Blog, BlogAdmin)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('subject','email')