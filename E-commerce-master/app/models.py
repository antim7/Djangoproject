from django.db import models

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import datetime

# Create your models here.
class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)

    def __str__(self):    #override
        return self.name


class Sub_Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Products(models.Model):
    Availability = (('In Stock','In Stock'),('Out of Stock','Out of Stock'))

    image = models.ImageField(upload_to='ecommerce/pimg')
    name = models.CharField(max_length=150)
    price = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=True)
    Availability = models.CharField(choices=Availability,null=True,max_length=150)
    details = models.TextField(null=True)

    def __str__(self):
        return self.name


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True,label='Email',error_messages={'exists': 'This Already Exists'})

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')

    #placeholder
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'


    def save(self, commit=True):            # defalt commit value true
        user = super(UserCreateForm, self).save(commit=False)
        '''it will return to the obj but not save in database.useful for custom process'''
        user.email = self.cleaned_data['email']  # valid or not
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(self.fields['email'].error_messages['exists'])
        return self.cleaned_data['email']


class Contact_us(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.email

class Order(models.Model):
    image = models.ImageField(upload_to='ecommerce/order/image')
    product = models.CharField(max_length=100,default='')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.CharField(max_length=10)
    total = models.CharField(max_length=100, default='')
    address = models.TextField()
    phone = models.CharField(max_length=10)
    transactionId = models.CharField(max_length=10)
    date = models.DateField(default=datetime.datetime.today)

    def __str__(self):
        return self.product

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)




