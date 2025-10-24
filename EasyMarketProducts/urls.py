from django.urls import path
from . import views
app_name = "EasyMarketProducts" 

urlpatterns = [
    path('scan/', views.scan_view, name='scan_view'),
    path('stop-scan/', views.stop_scan, name='stop_scan'),
    path('caissier-index/', views.show_caissier, name='caissier'),
    path('gestionnaire-index/', views.show_dashboard_gestionnaire, name='dashboard_gestionnaire'),
    path('produits/add-product/', views.add_product, name='add_product'),
    path("produits/<int:pk>/modifier/", views.product_update, name='product_update'),
    path("produits/<int:pk>/supprimer/", views.product_delete, name='product_delete'),
]