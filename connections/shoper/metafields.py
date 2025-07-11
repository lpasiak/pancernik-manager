import config
from tqdm import tqdm
import json
from utils.helpers.helper_functions import export_to_json


class ShoperMetafields:
    def __init__(self, client):
        """Initialize a Shoper Client
        https://developers.shoper.pl/developers/api/resources/metafields
        """
        self.client = client
        self.url = f'{self.client.site_url}/webapi/rest/metafields'

    def create_metafield(self, data: dict, object_type: str = 'product') -> int:
        """Create a new metafield.
        Args:
            data (dict): Data for the metafield to be created.
            object_type (str): Type of object to create metafield for. Default is 'product'.
        Returns:
            int: Identifier of the created metafield if successful
        """
        identifier = self.client._handle_request(
            'POST',
            f'{self.url}/{object_type}',
            json=data
        ).json()

        return identifier
    
    def get_metafield_by_id(self, identifier: str | int, object_type: str = 'product', export: bool = True) -> dict:
        """Get a metafield by its ID.
        Args:
            identifier (str|int): The ID of the metafield to retrieve.
            object_type (str): Type of object to get metafield for. Default is 'product'.
            export (bool): If True, export the metafield to a JSON file.
        Returns:
            dict: Metafield data if successful
        """
        data = self.client._handle_request('GET', f'{self.url}/{object_type}/{identifier}'
        ).json()
        
        if export:
            export_to_json(data, f'shoper/shoper_metafields-{identifier}.json')

        return data
    
    def get_all_metafields(self, object_type: str = 'product', export: bool = True) -> list[dict]:
        """Get all metafields.
        Args:
            object_type (str): Type of object to get metafields for. Default is 'product'.
            export (bool): If True, export the metafields to a JSON file.
        Returns:
            list: List of metafields if successful
        """
        metafields = []
        params = {
            'limit': config.SHOPER_LIMIT,
            'page': 1,
        }

        print("ℹ️  Downloading all metafields...")
        data = self.client._handle_request('GET', f'{self.url}/{object_type}', 
                                           params=params).json()
        
        number_of_pages = data.get('pages', 1)
        metafields.extend(data.get('list', []))

        for page in tqdm(range(2, number_of_pages + 1), 
                        desc='Downloading pages', unit=' page'):
            
            params['page'] = page
            data = self.client._handle_request('GET', f'{self.url}/{object_type}',
                                               params=params).json()
            metafields.extend(data.get('list', []))

        if export:
            export_to_json(data, f'shoper/shoper_metafields_{object_type}.json')

        return metafields
