from django.utils import timezone
from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, AbstractUser
)
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField



# # Model Person
# class Person(User): 
#     birth_date = models.DateField()
#     phone = models.CharField(max_length=15)
#     type_user = models.CharField(max_length=50, default="client")
# pip install django-phonenumber-field
    
    # def __str__(self) -> str:
    #     return self.first_name

    # @property
    # def full_name(self):
    #     "Returns the person's full name."
    #     return '%s %s' % (self.first_name, self.last_name)
    
    # class Meta:
    #     ordering = ["last_name", "first_name","birth_date","phone","email","type_user"]

# Model Abstract Room and Blog



class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username=models.CharField(max_length=25, unique=True)
    phone_number=PhoneNumberField(null=False, unique=True) # pip install django-phonenumber-field
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth','phone_number']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Room_Blog_Absact(models.Model):
    
    choice = (
            ('publised',  'PUBLISHED'),
             ( 'draft', 'DRAFT')
              )
    
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(blank=True, max_length=100, unique=True)
    description = models.TextField( )
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add =True)
    updated = models.DateTimeField(auto_now =True)
    status = models.CharField(choices= choice, max_length=50)
    services = TaggableManager() # user tag pip install django-taggit
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) :
        return self.title
    
    class Meta:
        #abstract = True i can't define this abstract class
        ordering = ['title','published','status','image']
    
        
# Model Comments for Room and Blog
class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    content = models.TextField()
    room_blog = models.ForeignKey(Room_Blog_Absact, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ('-created','name','email')

    def __str__(self):
        return 'Comment by {}'.format(self.name)
    
# Model chird Room for Room_Blog_Absact 
class Room(Room_Blog_Absact):
    price = models.IntegerField()
    size = models.IntegerField()
    capacity = models.IntegerField()
    bed = models.CharField(max_length=100,blank=True,null=True)
    
    class Meta:
        model: Room_Blog_Absact
        ordering = ('title','price','size','capacity','bed','published','status','image')
    

# Model Booking
class Reservation(models.Model):
    choice_guest = (
                    ('one_dult',  '1 Dult'),
                    ('two_dult',  '2 Dult'),
                    ('three_dult',  '3 Dult'),
                    ('four_dult',  '4 Dult'),
                    ('five_dult',  '5 Dult'),
                    ('two_dult_with_chirdeen',  '2 Dult 2 chirdeen'),
                    ('other','Other')
            
              )
    check_in = models.DateTimeField(auto_now_add =False)
    check_out = models.DateTimeField(auto_now_add =False)
    guest = models.CharField(choices= choice_guest, max_length=100)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
# Model Category    
class Category(models.Model):
    
    name = models.CharField(max_length=100,blank=True,null=True)
    
    def __str__(self):
        return self.name

# Model Chird Blog for Room_Blog_Absact      
class Blog(Room_Blog_Absact):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

# Model contact 

class Contact(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.email