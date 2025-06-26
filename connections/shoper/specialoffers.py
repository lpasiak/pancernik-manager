from .products import ShoperProducts
import config
from datetime import datetime
from tqdm import tqdm


class ShoperSpecialOffers:
    def __init__(self, client):
        """Initialize a Shoper Client
        https://developers.shoper.pl/developers/api/resources/specialoffers
        """
        self.client = client
        self.products = ShoperProducts(client)
        self.url = f'{self.client.site_url}/webapi/rest/specialoffers'
        self.TODAY = datetime.today().strftime('%Y-%m-%d')

    def create_special_offer(self, discount_data):
        """Create a special offer for in Shoper.
        Args:
            discount_data (dict): Data about the discount:
                product_id: integer,
                discount: float,
                discount_type: integer, (2 - fixed, 3 - percentage),
                date_to: dd-mm-YYYY

        Returns:
            int|dict: Special offer ID if successful, Error dict if failed
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

        if response.status_code != 200:
            error_description = response.json().get('error_description', 'Unknown error')
            return {'success': False, 'error': error_description}
        
        return response.json()

    def remove_special_offer_from_product(self, identifier, use_code=False):
        """Remove a special offer from Shoper.
        Args:
            identifier (int|str): Product ID or code (SKU)
            use_code (bool): Use product code (SKU) instead of product ID
        Returns:
            True|dict: True if successful, Error dict if failed
        """
        if use_code:
            product = self.products.get_product_by_code(identifier, use_code=True)
            promo_id = product.get('special_offer', {}).get('promo_id')
        else:
            product = self.products.get_product_by_code(identifier)
            promo_id = product.get('special_offer', {}).get('promo_id')

        if promo_id:
            response = self.client._handle_request(
                'DELETE',
                f'{self.url}/{promo_id}'
            )

            if response.status_code != 200:
                error_description = response.json()['error_description']
                return {'success': False, 'error': error_description}
        
            return True

        else:
            return {'success': False, 'error': 'No special offer found for this product.'}

    def get_all_special_offers(self):
        """Get all special offers from Shoper.
        Returns a Data list if successful, Error dict if failed"""
        special_offers = []
        params = {
            'limit': config.SHOPER_LIMIT,
            'page': 1
        }

        print("ℹ️  Downloading all special offers...")
        response = self.client._handle_request(
            'GET',
            self.url,
            params=params
        )

        if response.status_code != 200:
            error_description = response.json().get('error_description', 'Unknown error')
            return {'success': False, 'error': error_description}

        data = response.json()
        number_of_pages = data['pages']
        special_offers.extend(data.get('list', []))

        for page in tqdm(range(2, number_of_pages + 1),
                        desc="Downloading pages", unit=" page"):
            
            params['page'] = page
            response = self.client._handle_request(
                'GET',
                self.url,
                params=params
            )

            if response.status_code != 200:
                error_description = response.json().get('error_description', 'Unknown error')
                return {'success': False, 'error': error_description}

            special_offers.extend(response.json().get('list', []))

        return special_offers