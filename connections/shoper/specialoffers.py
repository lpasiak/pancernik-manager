from .products import ShoperProducts
import config
from datetime import datetime
from tqdm import tqdm
from utils.helpers.helper_functions import export_to_json


class ShoperSpecialOffers:
    def __init__(self, client):
        """Initialize a Shoper Client
        https://developers.shoper.pl/developers/api/resources/specialoffers
        """
        self.client = client
        self.products = ShoperProducts(client)
        self.url = f'{self.client.site_url}/webapi/rest/specialoffers'
        self.TODAY = datetime.today().strftime('%Y-%m-%d')

    def create_special_offer(self, discount_data: dict) -> int:
        """Create a special offer for in Shoper.
        Args:
            discount_data (dict): Data about the discount:
                product_id: integer,
                discount: float,
                discount_type: integer, (2 - fixed, 3 - percentage),
                date_to: dd-mm-YYYY

        Returns:
            int: Special offer ID if successful.
        """
        params = {
            'product_id': discount_data['product_id'],
            'discount': discount_data['discount'],
            'discount_type': discount_data['discount_type'],
            'date_from': self.TODAY,
            'date_to': discount_data['date_to'],
        }

        response = self.client._handle_request(
            'POST',
            self.url,
            json=params
        )
        
        return response.json()

    def get_all_special_offers(self, export: bool = True) -> list[dict]:
        """Get all special offers from Shoper.
        Args:
            export (bool): If True, export the special offers to a JSON file.
        Returns:
            list: List of special offers if successful.
        """
        special_offers = []
        params = {
            'limit': config.SHOPER_LIMIT,
            'page': 1
        }

        print("ℹ️  Downloading all special offers...")
        data = self.client._handle_request('GET', self.url, params=params).json()
        number_of_pages = data.get('pages', 1)
        special_offers.extend(data.get('list', []))

        for page in tqdm(range(2, number_of_pages + 1),
                        desc="Downloading pages", unit=" page"):
            
            params['page'] = page
            data = self.client._handle_request('GET', self.url, params=params).json()
            special_offers.extend(data.get('list', []))

        if export:
            export_to_json(special_offers, 'shoper/shoper_special_offers.json')

        return special_offers
    
    def remove_special_offer_from_product(self, identifier: str | int, use_code: bool = False) -> bool:
        """Remove a special offer from Shoper.
        Args:
            identifier (str): Product ID or code (SKU).
            use_code (bool): Use product code (SKU) instead of product ID.
        Returns:
            True: True if successful.
        """
        product = self.products.get_product_by_code(identifier, use_code=use_code)
        promo_id = product.get('special_offer', {}).get('promo_id')
        
        self.client._handle_request('DELETE', f'{self.url}/{promo_id}')
        return True
