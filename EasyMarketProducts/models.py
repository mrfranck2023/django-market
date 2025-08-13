from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom du produit")
    barcode = models.CharField(max_length=50, unique=True, verbose_name="Code-barres")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock")

    def __str__(self):
        return f"{self.name} - {self.barcode}"
