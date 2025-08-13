from django.urls import path
from . import views
app_name = "EasyMarketProducts" 

urlpatterns = [
    path('scan/', views.scan_view, name='scan_view'),
    path('stop-scan/', views.stop_scan, name='stop_scan'),
    path('caissier-index/', views.show_caissier, name='caissier'),
]