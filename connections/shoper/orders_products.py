import config
from tqdm import tqdm
from datetime import datetime


class ShoperProductOrders:
    def __init__(self, client):
        """Initialize a Shoper Client
        https://developers.shoper.pl/developers/api/resources/order-products
        """
        self.client = client
        self.url = f'{self.client.site_url}/webapi/rest/order-products'

    def get_latest_product_orders(self, pages_to_fetch=1):
        """Get latest product orders from Shoper.
        Args:
            pages_to_fetch (int): Number of pages to fetch, default is 1.
        Returns:
            list|dict: Data list if successful, Error dict if failed
        """
        order_products = []
        params = {
            'limit': config.SHOPER_LIMIT,
            'page': 1
        }

        print(f"ℹ️  Downloading latest product orders...")
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

        if pages_to_fetch > number_of_pages:
            error_description = 'Requested number of pages exceeds available data.'
            return {'success': False, 'error': error_description}

        # We need to fetch the newest products, so we start from the last page and decrement
        start_page = number_of_pages
        end_page = number_of_pages - pages_to_fetch + 1

        for page in tqdm(range(start_page, end_page - 1, -1),
                         desc="Downloading pages", unit=' page'):

            params['page'] = page
            response = self.client._handle_request(
                'GET',
                self.url,
                params=params)
            
            if response.status_code != 200:
                error_description = response.json().get('error_description', 'Unknown error')
                return {'success': False, 'error': error_description}

            order_products.extend(response.json().get('list', []))

        return order_products
