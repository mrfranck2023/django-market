from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import Product
import cv2
from pyzbar.pyzbar import decode
import threading
import pygame
import os
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

# Initialize pygame mixer
pygame.mixer.init()
sound_file_path = os.path.join(os.path.dirname(__file__), 'be.wav')
scanned_barcodes = []

def play_sound():
    pygame.mixer.music.load(sound_file_path)
    pygame.mixer.music.play()

scanning_active = True

def barcode_scanner():
    global scanning_active
    channel_layer = get_channel_layer()

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erreur : Impossible d'ouvrir la webcam")
        return

    while cap.isOpened() and scanning_active:
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
                if barcode_data and barcode_data not in scanned_barcodes:
                    cv2.putText(frame, barcode_data, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 255), 2)
                    print(f"Code-barres détecté : {barcode_data}")
                    scanned_barcodes.append(barcode_data)
                    play_sound()
                    async_to_sync(channel_layer.group_send)(
                        'barcode_group',
                        {
                            'type': 'receive',
                            'barcode': barcode_data
                        }
                    )

        cv2.imshow("scanner", frame)
        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

def scan_view(request):
    global scanning_active
    scanning_active = True
    scanning_thread = threading.Thread(target=barcode_scanner)
    scanning_thread.start()
    return HttpResponse("Barcode scanning started. Visit '/stop-scan/' to stop scanning.")

def stop_scan(request):
    global scanning_active
    scanning_active = False
    return HttpResponse("Barcode scanning stopped.")

def show_caissier(request):
    products = Product.objects.filter(barcode__in=scanned_barcodes)
    return render(request, "EasyMarketProducts/caissier_index.html", {"produits": products})