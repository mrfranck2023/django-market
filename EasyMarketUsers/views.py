from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect


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

        
    
    return render(request, "EasyMarketUsers/login.html")

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
                user = User.objects.create_user(username=username, password=password, statut=statut)
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