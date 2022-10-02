from django.contrib import admin
from .models import Person, Room,Booking, Category, Blog



# Model admin person.
class PersonAdmin(admin.ModelAdmin):
    pass
admin.site.register(Person, PersonAdmin)

# Model Admin room and booking
class RoomAdmin(admin.ModelAdmin):
    pass
admin.site.register(Room, RoomAdmin)
admin.site.register(Booking, RoomAdmin)

# Model admin blog by category
class BlogAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, BlogAdmin)
admin.site.register(Blog, BlogAdmin)