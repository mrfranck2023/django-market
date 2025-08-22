from django.urls import path
from . import views
app_name = "EasyMarketUsers" 

urlpatterns = [
    path('login/', views.login_user, name = 'login'),
    path('logout/', views.logout_user, name = 'logout'),
    path('register/', views.register_user, name = 'register'),
    path('index/', views.index, name = 'index'),
    path("api/etat-caisse/", views.etat_caisse, name="etat_caisse"),
    path("api/check-user/", views.check_user, name="check_user"),
]
