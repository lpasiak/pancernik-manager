from .pictures import ShoperPictures
import config, json
from tqdm import tqdm


class ShoperProducts:
    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client
        self.pictures = ShoperPictures(client)

    def get_product_by_code(self, identifier, pictures=False, use_code=False):
        """Get a product from Shoper by either product ID or product code.
        Args:
            identifier (int|str): Product ID (int) or product code (str)
            use_code (bool): If True, use product code (SKU) instead of ID
        Returns:
            dict: Product data if successful, Error dict if failed
        """
        
        if use_code:
            # Get product by product code (SKU)
            product_filter = {
                "filters": json.dumps({"stock.code": identifier})
            }
            response = self.client._handle_request(
                'GET',
                f'{self.client.site_url}/webapi/rest/products',
                params=product_filter
            )
            product_list = response.json().get('list', [])

            if not product_list:
                return {'success': False,
                        'error': f'Product {identifier} doesn\'t exist'}

            product = product_list[0]
            
        else:
            # Get product by product ID
            response = self.client._handle_request(
                'GET',
                f'{self.client.site_url}/webapi/rest/products/{identifier}'
            )
            product = response.json()
            
            if response.status_code != 200:
                error_description = response.json().get('error_description', 'Unknown error')
                return {'success': False, 'error': error_description}

        # Get product pictures if requested
        if pictures:
            try:
                product['img'] = self.pictures.get_product_pictures(product['product_id'])
            except Exception as e:
                product['img'] = []

        return product

    def create_product(self, product_data):
        """Create a new product in Shoper
        Args:
            product_data (dict): Product data | 
            https://developers.shoper.pl/developers/api/resources/products/insert
        Returns:
            int|dict: Product ID if successful, Error dict if failed
        """
        response = self.client._handle_request(
            'POST', f'{self.client.site_url}/webapi/rest/products', 
            json=product_data
        )
        
        if response.status_code != 200:
            error_description = response.json().get('error_description', 'Unknown error')
            return {'success': False, 'error': error_description}
        
        product_id = response.json()

        if isinstance(product_id, int):
            return product_id
        else:
            return {'success': False,
                    'error': 'Response is not an integer, check the API response.'}

    def remove_product(self, product_id):
        """Remove a product from Shoper
        Args:
            product_id (int): Product id
        Returns:
            True|dict: True if successful, Error dict if failed
        """
        response = self.client._handle_request(
            'DELETE',
            f'{self.client.site_url}/webapi/rest/products/{product_id}'
        )
        
        if response.status_code != 200:
            error_description = response.json().get('error_description', 'Unknown error')
            return {'success': False, 'error': error_description}
        
        return True

    def update_product_by_code(self, identifier, use_code=False, **parameters):
        """Update a product from Shoper. Returns True if successful, None if failed
        Args:
            identifier (int|str): Product id or product code
            use_code (bool): If True, use product code (SKU) instead of ID
            parameters key=value: Parameters to update
            https://developers.shoper.pl/developers/api/resources/products/update
        Returns:
            True|dict: True if successful, Error dict if failed
        """
        if use_code:
            # Get product id by product code (SKU)
            product = self.get_product_by_code(identifier, use_code=True)
            product_id = product['product_id']
        else:
            product_id = identifier

        params = {}

        for key, value in parameters.items():
            if value is not None:
                params[key] = value
        response = self.client._handle_request(
            'PUT',
            f'{self.client.site_url}/webapi/rest/products/{product_id}',
            json=params
        )

        if response.status_code != 200:
            error_description = response.json().get('error_description', 'Unknown error')
            return {'success': False, 'error': error_description}
        
        return True

    def get_all_products(self):
        """Get all products from Shoper.
        Returns a Data dict if successful, Error dict if failed"""
        products = []
        url = f'{self.client.site_url}/webapi/rest/products'
        params = {
            'limit': config.SHOPER_LIMIT,
            'page': 1
        }

        print("ℹ️  Downloading all products...")
        response = self.client._handle_request('GET', url, params=params)

        if response.status_code != 200:
            error_description = response.json().get('error_description', 'Unknown error')
            return {'success': False, 'error': error_description}

        data = response.json()
        number_of_pages = data['pages']
        products.extend(data.get('list', []))

        for page in tqdm(range(2, number_of_pages + 1),
                         desc="Downloading pages", unit=" page"):
            
            params['page'] = page
            response = self.client._handle_request('GET', url, params=params)

            if response.status_code != 200:
                error_description = response.json().get('error_description', 'Unknown error')
                return {'success': False, 'error': error_description}

            page_data = response.json().get('list', [])
            products.extend(page_data)

        return products
