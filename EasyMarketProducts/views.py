from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product
import cv2
from pyzbar.pyzbar import decode
import threading
import pygame
import os
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import time


#------------------------------------- implémentation du scan de QR code ------------------------------------------------------
# Initialize pygame mixer
pygame.mixer.init()
sound_file_path = os.path.join(os.path.dirname(__file__), 'be.wav')

# Dictionnaire pour suivre l'état du scan par utilisateur
scanning_active_by_user = {}
last_scan_time_by_user = {}
lock = threading.Lock()  # Verrou pour protéger l'accès au dictionnaire

def play_sound():
    pygame.mixer.music.load(sound_file_path)
    pygame.mixer.music.play()

def barcode_scanner(request):
    channel_layer = get_channel_layer()
    user_id = request.user.id
    scanned_barcodes = request.session.get('scanned_barcodes', [])
    print(f"Début du scan pour l'utilisateur {user_id}")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erreur : Impossible d'ouvrir la webcam")
        return

    with lock:
        scanning_active_by_user[user_id] = True  # Initialiser l'état pour cet utilisateur

    while cap.isOpened():
        with lock:
            if not scanning_active_by_user.get(user_id, False):
                break  # Arrêter si scanning_active_by_user[user_id] est False

        success, frame = cap.read()
        if not success:
            print("Erreur : Impossible de lire le flux vidéo")
            break

        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (640, 480))

        detectedBarcode = decode(frame)

        if not detectedBarcode:
            print("Aucun code-barres détecté")
        else:
            for barcode in detectedBarcode:
                barcode_data = str(barcode.data.decode('utf-8'))
                if barcode_data:
                    cv2.putText(frame, barcode_data, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 255), 2)
                    print(f"Code-barres détecté : {barcode_data}")
                    scanned_barcodes.append(barcode_data)
                    request.session['scanned_barcodes'] = scanned_barcodes
                    request.session.modified = True
                    now = time.time()
                    last_time = last_scan_time_by_user.get(user_id, 0)

                    if now - last_time > 5:   # 1 seconde entre scans
                        print("ouiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
                        valeur = now - last_time
                        print(last_time)
                        print(valeur)
                        last_scan_time_by_user[user_id] = now
                        async_to_sync(channel_layer.group_send)(
                            f"barcode_group_{user_id}",
                            {
                                'type': 'product_message',
                                'barcode': barcode_data
                            }
                        )
                        play_sound()

        cv2.imshow("scanner", frame)
        if cv2.waitKey(1) == ord("q"):
            with lock:
                scanning_active_by_user[user_id] = False
            break

    cap.release()
    cv2.destroyAllWindows()
    with lock:
        scanning_active_by_user.pop(user_id, None)  # Nettoyer après arrêt

@login_required
def scan_view(request):

    user_id = request.user.id

    # IMPORTANT : réactiver le scan pour cet utilisateur
    with lock:
        scanning_active_by_user[user_id] = True

    scanning_thread = threading.Thread(
        target=barcode_scanner,
        args=(request,),
        daemon=True   # évite les bugs au redémarrage
    )

    scanning_thread.start()

    return HttpResponse("Scan démarré")

@login_required
def stop_scan(request):
    user_id = request.user.id
    with lock:
        scanning_active_by_user[user_id] = False  # Arrêter le scan pour cet utilisateur
    return HttpResponse("Barcode scanning stopped.")


#------------------------------------- implémentation du scan de QR code ------------------------------------------------------



@login_required
def show_caissier(request):
    scanned_barcodes = request.session.get('scanned_barcodes', [])
    products = Product.objects.filter(barcode__in=scanned_barcodes)
    return render(request, "EasyMarketProducts/caissier_index.html", {"produits": products})


# dans ce code on utilise les session pour scanner et garder pour chaque utilisateur les produits qu'ili a scanné dans sa propre session





def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return JsonResponse({
                "success": True,
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "price": str(product.price),
                    "stock": product.stock,
                }
            })
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = ProductForm()
        return render(request, "EasyMarketProducts/add_product_form.html", {"form": form})



def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    return render(request, "EasyMarketProducts/add_product_form.html", {"form": form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return JsonResponse({'success': True})
    return render(request, "EasyMarketProducts/delete.html", {"product": product})






@login_required
def show_dashboard_gestionnaire(request):
    products = Product.objects.all()
    return render(request, "EasyMarketProducts/gestionnaire_index.html", {"products": products})
