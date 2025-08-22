from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Caisse

User = get_user_model()

def index(request):
    return render(request, "EasyMarketUsers/index.html")

def login_user(request):
    if request.method == "POST":
        username =  request.POST.get("username")
        password = request.POST.get("password") 

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect("EasyMarketUsers:index")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")

        
    gestionnaire = User.objects.get(statut = "gestionnaire")
    donnee = {
        "nbre_caisse": gestionnaire.nbr_caisse
    }
    donnee['caisse_range'] = list(range(1, donnee['nbre_caisse'] + 1))

    context = {"donnee":donnee}
    return render(request, "EasyMarketUsers/login.html", context)

def etat_caisse(request):
    numero = request.GET.get("numero")
    if not numero:
        return JsonResponse({"etat": None, "message": ""})

    try:
        caisse = Caisse.objects.get(numero=numero)
        if caisse.etat == "ouverte":
            return JsonResponse({"etat": "occupee", "message": f"La caisse {numero} est déjà occupée"})
        else:
            return JsonResponse({"etat": "libre", "message": f"La caisse {numero} est libre"})
    except Caisse.DoesNotExist:
        return JsonResponse({"etat": "inexistante", "message": f"La caisse {numero} n'existe pas"})
    
def check_user(request):
    numero = request.GET.get("numero")
    code_admin = "123"
    code_gestionnaire = "321"
    code_caissier = "12345"
    if not numero:
        return JsonResponse({"etat": None, "message": ""})

    try:
        if code_caissier == numero:
            return JsonResponse({"etat": "", "is_caissier": True})
        else:
            return JsonResponse({"etat": "", "is_caissier": False})
    except Caisse.DoesNotExist:
        return JsonResponse({"etat": "inexistante", "message": f"Le numero {numero} n'existe pas"})
    

def logout_user(request):
    logout(request)
    return redirect("EasyMarketUsers:index") 
    # lorsque tu créera une autre application et tu lui octroira un nom nom tu fera une redirection telle que celle ci     return redirect("nomapplication:index") 
 

# def register_user(request):
#     if request.method == "POST":
#         form = InscriptionForm(request.POST)

#         if form.is_valid():
#             form.save()
#             return redirect("mangalib:index")
    
#     else:
#         form = InscriptionForm()

#     return render(request, "EasyMarketUsers/register.html", {"form": form})

def register_user(request):
    code_admin = "123"
    code_gestionnaire = "321"
    code_caissier = "12345"
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        statut = request.POST.get("statut") 
        nbre_caisse = request.POST.get("caisse_numbers", 1)
        code_utilisateur = request.POST.get("token") 

        if statut == "admin":
            if code_utilisateur == code_admin:
                user = User.objects.create_user(username=username, password=password, statut=statut)
                login(request, user)
                return redirect("EasyMarketUsers:index")
            else:
                messages.info(request, "Ce code ne vous appartient pas !")

        elif statut == "gestionnaire":
            if code_utilisateur ==code_gestionnaire:
                user = User.objects.create_user(username=username, password=password, statut=statut, nbr_caisse=nbre_caisse)
                login(request, user)
                return redirect("EasyMarketUsers:index")
            else:
                messages.info(request, "Ce code ne vous appartient pas !")

        elif statut == "caissier":
            if code_utilisateur == code_caissier:
                user = User.objects.create_user(username=username, password=password, statut=statut)
                login(request, user)
                return redirect("EasyMarketUsers:index")
            else:
                messages.info(request, "Ce code ne vous appartient pas !")

    return render(request, "EasyMarketUsers/register.html")