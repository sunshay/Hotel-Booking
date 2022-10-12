from django import forms
from .models import Comment, Contact
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from phonenumber_field.formfields import PhoneNumberField

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'content')
        

class ContactForm(forms.ModelForm):
    #number = PhoneNumberField(region="CA")
    class Meta:
        model = Contact
        fields = ('name','phone', 'email', 'subject','message')
        
        # widgets = {
        #     'phone': PhoneNumberPrefixWidget(),
        # }