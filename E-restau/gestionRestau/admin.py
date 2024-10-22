from django.contrib import admin
from .models import *
# Register your models here.
class MenuAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category")
    search_fields = ("name",)
    list_filter = ("category",)
admin.site.register(Menu, MenuAdmin)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "is_staff")
    list_editable = ("is_staff",)
    search_fields = ("username",)
admin.site.register(CustomUser, CustomUserAdmin)

class CommandeAdmin(admin.ModelAdmin):
    list_display = ("client", "message", "date", "commentaire", "type", "total")
    search_fields = ("client", "menu")
    list_filter = ("type",)
admin.site.register(Commande, CommandeAdmin)
