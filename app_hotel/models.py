import email
from django.utils import timezone
from django.db import models
from taggit.managers import TaggableManager


# Model Person
class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    type_user = models.CharField(max_length=50, default="client")
    
    def __str__(self) -> str:
        return self.first_name

    @property
    def full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)
    
    class Meta:
        ordering = ["last_name", "first_name","birth_date","phone","email","type_user"]

# Model Abstract Room and Blog
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
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    
    def __str__(self) :
        return self.title
    
    class Meta:
        #abstract = True
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
class Booking(models.Model):
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
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    
# Model Category    
class Category(models.Model):
    
    name = models.CharField(max_length=100,blank=True,null=True)
    
    def __str__(self):
        return self.name

# Model Chird Blog for Room_Blog_Absact      
class Blog(Room_Blog_Absact):
    room_blog = models.ForeignKey(Category, on_delete=models.CASCADE)