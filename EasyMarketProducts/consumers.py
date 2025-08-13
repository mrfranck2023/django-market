from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async

class BarcodeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('barcode_group', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('barcode_group', self.channel_name)

    async def receive(self, text_data):
        from .models import Product  # Importer ici pour éviter l'initialisation prématurée
        # Vérifier si text_data est un dictionnaire ou une chaîne
        if isinstance(text_data, dict):
            text_data_json = text_data
        else:
            text_data_json = json.loads(text_data)

        barcode = text_data_json.get('barcode')

        if not barcode:
            await self.send(text_data=json.dumps({
                'error': 'Aucun code-barres fourni'
            }))
            return

        try:
            # Utiliser sync_to_async pour la requête synchrone
            product = await sync_to_async(Product.objects.get)(barcode=barcode)
            product_data = {
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'barcode': product.barcode,
            }
            await self.channel_layer.group_send(
                'barcode_group',
                {
                    'type': 'product_message',
                    'product': product_data
                }
            )
        except Product.DoesNotExist:
            await self.send(text_data=json.dumps({
                'error': f'Produit avec code-barres {barcode} non trouvé'
            }))

    async def product_message(self, event):
        product = event['product']
        await self.send(text_data=json.dumps({
            'product': product
        }))