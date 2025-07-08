from connections.gsheets import GSheetsClient, GsheetsWorksheets
from connections.shoper import ShoperAPIClient, ShoperPictures, ShoperProducts
from connections.allegro import AllegroAPIClient, AllegroOffers
from pprint import pprint
import pandas as pd
import json
import config

allegro_client = AllegroAPIClient()
allegro_client.connect()

allegro_offers = AllegroOffers(allegro_client)

# gsheets_client = GSheetsClient('14KXydCTaBwpB4un6iEQSj9XTzKOQ0nLfHe_yxmPd43s')
# gsheets_client.connect()
# gsheets_worksheets = GsheetsWorksheets(gsheets_client)

# x = gsheets_worksheets.batch_remove_data('test3', [8, 9, 7])
# print(x)

# client = ShoperAPIClient()
# client.connect()

# sh_pictures = ShoperPictures(client)
# sh_products = ShoperProducts(client)


"""
data = {
    'name': 'Testowy produkt taki o hehe',
    'description': {
        'sections': [
            {
                'items': [
                    {
                        'type': 'TEXT',
                        'content': '<h1>Testowy opisik fiu fiu.</h1>'
                    }
                ]
            }
        ]
    }
}
"""