import config
from tqdm import tqdm
import json


class ShoperMetafieldValues:
    def __init__(self, client):
        """Initialize a Shoper Client
        https://developers.shoper.pl/developers/api/resources/metafield-values
        """
        self.client = client
        self.url = f'{self.client.site_url}/webapi/rest/metafield-values'