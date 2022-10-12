from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import Contact, Room,Comment,Reservation, Category, Blog, User
from django.utils.html import format_html

# change Django administration text Login, The listview page and The HTML title tag 
admin.site.site_header = "Hotel Booking"
admin.site.site_title = "Hotel Booking Admin Penal"
admin.site.index_title = "Welcome to Hotel Booking"
    

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','phone_number','email', 'date_of_birth')
        
        # widgets = {
        #     'phone_number': PhoneNumberPrefixWidget(),
        # }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username','phone_number','email', 'password', 'date_of_birth', 'is_active', 'is_admin')


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username','phone_number','email', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username','phone_number','date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','phone_number','email', 'date_of_birth', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()





# # Model admin person. 
# ... and, since we're not using Django's built-in permissions,
# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# class UserAdmin(admin.ModelAdmin):
#     #list_display = ('username','phone_number','email', 'date_of_birth', 'is_admin')
#     pass

# unregister the Group model from admin.
admin.site.unregister(Group)
# class GroupAdmin(admin.ModelAdmin):
#     #list_display = ('username','phone_number','email', 'date_of_birth', 'is_admin')
#     pass



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

# model contact public
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','phone','subject','email')

# model Reservation room    
@admin.register(Reservation)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('check_in','check_out','room','number_guest','user',)