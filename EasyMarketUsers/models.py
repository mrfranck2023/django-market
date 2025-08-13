from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilisateurs(AbstractUser):

    statut = models.CharField(max_length= 64)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

