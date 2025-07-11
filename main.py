from connections.gsheets import GSheetsClient, GsheetsWorksheets
from connections.shoper import ShoperAPIError
from connections.shoper import (ShoperAPIClient, 
                                ShoperPictures,
                                ShoperSpecialOffers,
                                ShoperCategories, 
                                ShoperProducts, 
                                ShoperRedirects, 
                                ShoperMetafields,
                                ShoperMetafieldValues,
                                ShoperGauges)

from connections.allegro import AllegroAPIClient, AllegroOffers
from pprint import pprint
import pandas as pd
import json
import config


client = ShoperAPIClient()
client.connect()
sh_products = ShoperProducts(client)
sh_special_offers = ShoperSpecialOffers(client)
sh_redirects = ShoperRedirects(client)
sh_categories = ShoperCategories(client)
sh_gauges = ShoperGauges(client)
sh_images = ShoperPictures(client)

try:
    sh_images.get_product_pictures(product_id=101, export=True)
except ShoperAPIError as e:
    print(f"Error: {e}")



















# allegro_client = AllegroAPIClient()
# allegro_client.connect()

# allegro_offers = AllegroOffers(allegro_client)

# gsheets_client = GSheetsClient('14KXydCTaBwpB4un6iEQSj9XTzKOQ0nLfHe_yxmPd43s')
# gsheets_client.connect()
# gsheets_worksheets = GsheetsWorksheets(gsheets_client)

# x = gsheets_worksheets.batch_remove_data('test3', [8, 9, 7])
# print(x)

# sh_metafields = ShoperMetafields(client)

# try:
#     metafield = sh_metafields.get_metafield_by_id(identifier=1000, object_type='product')
# except ShoperAPIError as e:
#     print(f"Error: {e}")
# except Exception as e:
#     print(f"An unexpected error occurred: {e}")

# metafield_data = {
#     'object': 'Product',
#     'namespace': 'product_compatibility',
#     'key': 'compatibility',
#     'description': 'Product Compatibility (device models) - Pasiak',
#     'type': 3,
# }

# x = sh_metafields.create_metafield(
#     data=metafield_data,
#     object_type='product')

