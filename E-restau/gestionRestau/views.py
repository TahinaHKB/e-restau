from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from gestionRestau.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.generic import ListView, CreateView
from django.db.models import Sum
# Create your views here.
class customSignUpForm ( UserCreationForm ): 
    class Meta : 
        model = CustomUser 
        fields = UserCreationForm.Meta.fields
def SignUpPage (request) : 
    context = {}

    if request.method == "POST" : 
        form = customSignUpForm(request.POST)
        if form.is_valid() :
            form.save()
            return redirect("/account/login/")
        else :
            context['errors'] = form.errors
    
    form = customSignUpForm()
    context['form'] = form

    return render(request, "SignUp.html", context=context)

def Home(request) : 
    if not request.user.is_authenticated : 
        return redirect("/account/login/")
    if request.user.is_superuser : 
        superuser = True
    else : 
        superuser = False
    return render(request, "Home.html", {"username" : request.user.username, "superuser" : superuser})

def Deconnexion(request) : 
    logout(request)
    return redirect("/account/login/")

class MenuListView(ListView) : 
    model = Menu
    template_name = "Menu/menu.html"
    context_object_name = "post"

class MenuAddView(CreateView) : 
    model = Menu
    template_name = "Menu/menuAdd.html"
    success_url = reverse_lazy('menu')
    form_class = MenuForm

def MenuList(request) : 
    menuData = Menu.objects.all().order_by("category")
    menu = {}
    cat = ""
    for m in menuData : 
        if cat != m.category : 
            temp = {"name":m.name, "price":m.price, "pk":m.pk}
            menu[m.category] = [temp]
            cat = m.category
        else :
            temp = {"name":m.name, "price":m.price, "pk":m.pk}
            menu[m.category].append(temp)
    if Commande.objects.filter(type="attente", client=request.user).exists() : 
        ajout = True
    else : 
        ajout = False
    return render(request, "Menu/menu.html", {"menu":menu, "ajout":ajout})

def ajoutCommandeMenu(request, pk) :
    if Commande.objects.filter(type="attente", client=request.user).exists() : 
        com = Commande.objects.get(type="attente", client=request.user)
        menu = Menu.objects.get(pk=pk)
        com.menu.add(menu)
    return redirect("/menu/")

def commande(request) :
     somme = 0
     if Commande.objects.filter(type="attente", client=request.user).exists() : 
        com = Commande.objects.get(type="attente", client=request.user)
        for c in com.menu.all() :
            somme += c.price
        form = CommandeForm()
     else : 
         com = None
         form = None
     return render(request, "Menu/commande.html", {"commande": com, "total":somme, "form":form})

def createCommande(request) : 
    com = Commande(client=request.user, type="attente")
    com.save()
    return redirect("/commande/")

def modifyCommande(request) : 
    if request.method == "POST" : 
        com = Commande.objects.get(type="attente", client=request.user)
        somme = 0
        for c in com.menu.all() :
            somme += c.price
        com.message = request.POST.get('msg')
        com.commentaire = request.POST.get('commentaire')
        com.type = "envoye"
        com.total = somme
        com.save()
    return redirect("/commande/")

def gererCommande(request):
    commande = Commande.objects.exclude(type="attente").order_by("client", "date")
    return render(request, "gestionCommande.html", {"com" : commande })

def confirmCommande(request, pk):
    commande = Commande.objects.get(pk=pk)
    commande.type = "confirmé"
    commande.save()
    return redirect("/gestionCommande/")

def redirection(request):
    return redirect("/account/login")