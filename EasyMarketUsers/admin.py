from django.contrib import admin

from EasyMarketUsers.models import Utilisateurs, Caisse, SessionCaisse

@admin.register(Utilisateurs) #ce decorateur permet de se passer de ce code admin.site.register(Book, BookAdmin)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'statut')


@admin.register(Caisse) #ce decorateur permet de se passer de ce code admin.site.register(Book, BookAdmin)
class CaisseAdmin(admin.ModelAdmin):
    list_display = ('numero', 'etat', 'montant')

@admin.register(SessionCaisse) #ce decorateur permet de se passer de ce code admin.site.register(Book, BookAdmin)
class SessionCaisseAdmin(admin.ModelAdmin):
    list_display = ('caisse', 'caissier', 'date_ouverture', 'date_fermeture', 'montant_session')