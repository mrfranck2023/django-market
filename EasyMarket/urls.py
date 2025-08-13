from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('easyMarketUsers/', include('EasyMarketUsers.urls')),
    path('easyMarketProducts/', include('EasyMarketProducts.urls'))
]
