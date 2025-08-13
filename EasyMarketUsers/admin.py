from django.contrib import admin

from EasyMarketUsers.models import Utilisateurs

@admin.register(Utilisateurs) #ce decorateur permet de ce passer de ce code admin.site.register(Book, BookAdmin)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'statut')


