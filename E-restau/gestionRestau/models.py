from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
# Create your models here.

class CustomUser(AbstractUser): 
    pass

class Menu(models.Model): 
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.CharField(max_length=100)

class MenuForm(forms.ModelForm): 
    class Meta : 
        model = Menu
        fields = [
            'name', 'price', 'category'
        ]

class Commande(models.Model):
    client = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    menu = models.ManyToManyField(Menu)
    date = models.DateField(auto_now = True)
    message = models.TextField(blank = False)
    commentaire = models.TextField(blank = True)
    total = models.IntegerField(default=0)
    type = models.CharField(max_length=20)

class CommandeForm(forms.ModelForm): 
    class Meta : 
        model = Commande
        fields = [
            'message', 'commentaire'
        ]
