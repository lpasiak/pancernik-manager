from .pictures import ShoperPictures
import config, json
from tqdm import tqdm


class ShoperProducts:
    def __init__(self, client):
        """Initialize a Shoper Client
        https://developers.shoper.pl/developers/api/resources/products
        """
        self.client = client
        self.pictures = ShoperPictures(client)
        self.url = f'{self.client.site_url}/webapi/rest/products'

    def get_product_by_code(self, identifier: str, pictures: bool = False, use_code: bool = False) -> dict:
        """Get a product from Shoper by either product ID or product code.
        Args:
            identifier (str): Product ID (int) or product code (str)
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
                self.url,
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
                f'{self.url}/{identifier}'
            )
            product = response.json()
            
            if response.status_code != 200:
                error_description = response.json().get('error_description', 'Unknown error')
                return {'success': False, 'error': error_description}

        # Get product pictures if requested
        if pictures:
            try:
                product['img'] = self.pictures.get_product_pictures(product['product_id'])
            except Exception:
                product['img'] = []

        return product

    def create_product(self, product_data: dict) -> int | dict:
        """Create a new product in Shoper
        Args:
            product_data (dict): Product data
        Returns:
            int|dict: Product ID if successful, Error dict if failed
        """
        response = self.client._handle_request(
            'POST',
            self.url,
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

    def remove_product(self, product_id: str) -> bool | dict:
        """Remove a product from Shoper
        Args:
            product_id (str): Product id
        Returns:
            True|dict: True if successful, Error dict if failed
        """
        response = self.client._handle_request(
            'DELETE',
            f'{self.url}/{product_id}'
        )
        
        if response.status_code != 200:
            error_description = response.json().get('error_description', 'Unknown error')
            return {'success': False, 'error': error_description}
        
        return True

    def update_product_by_code(self, identifier: str, use_code: bool = False, **parameters) -> bool | dict:
        """Update a product from Shoper. Returns True if successful, None if failed
        Args:
            identifier (str): Product id or product code
            use_code (bool): If True, use product code (SKU) instead of ID
            parameters key=value: Parameters to update
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
            f'{self.url}/{product_id}',
            json=params
        )

        if response.status_code != 200:
            error_description = response.json().get('error_description', 'Unknown error')
            return {'success': False, 'error': error_description}
        
        return True

    def get_all_products(self) -> list | dict:
        """Get all products from Shoper.
        Returns a Data list if successful, Error dict if failed"""
        products = []
        params = {
            'limit': config.SHOPER_LIMIT,
            'page': 1
        }

        print("ℹ️  Downloading all products...")
        response = self.client._handle_request(
            'GET',
            self.url,
            params=params
        )
        print(response)
        if response.status_code != 200:
            error_description = response.json().get('error_description', 'Unknown error')
            return {'success': False, 'error': error_description}

        data = response.json()
        number_of_pages = data['pages']
        products.extend(data.get('list', []))

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

            products.extend(response.json().get('list', []))

        return products
