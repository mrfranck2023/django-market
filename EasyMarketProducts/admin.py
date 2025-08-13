from django.contrib import admin

from EasyMarketProducts.models import Product

@admin.register(Product) #ce decorateur permet de ce passer de ce code admin.site.register(Book, BookAdmin)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'barcode', 'price', 'stock')


