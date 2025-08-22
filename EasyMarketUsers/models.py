from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from decimal import Decimal
from django.conf import settings



class Utilisateurs(AbstractUser):
    nbr_caisse = models.IntegerField(null=True, blank=True)
    statut = models.CharField(max_length= 64)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

class Caisse(models.Model):
    numero = models.CharField(max_length=10)
    etat = models.CharField(max_length=10, default="fermée")  # fermée / ouverte
    montant = models.DecimalField(max_digits=20, decimal_places=2, default=0)

class SessionCaisse(models.Model):
    caisse = models.ForeignKey(Caisse, on_delete=models.SET_NULL, null=True)
    caissier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    date_ouverture = models.DateTimeField(auto_now_add=True)
    date_fermeture = models.DateTimeField(null=True, blank=True)
    montant_session = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    # montant_final = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Session {self.id} - {self.caisse.numero} ({self.caissier})"

    def ouvrir_session(self):
        self.caisse.etat = "ouverte"
        self.caisse.save()

    def fermer_session(self, montant_final):
        self.date_fermeture = timezone.now()
        self.montant_final = montant_final
        self.save()
        self.caisse.etat = "fermée"
        self.caisse.save()