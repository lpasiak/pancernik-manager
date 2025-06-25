from connections.shoper import ShoperAPIClient, ShoperAttributes, ShoperPictures
from pprint import pprint
import json

client = ShoperAPIClient()
client.connect()

attributes = ShoperAttributes(client)
pictures = ShoperPictures(client)

x = pictures.get_product_pictures("XD")
print(x)


