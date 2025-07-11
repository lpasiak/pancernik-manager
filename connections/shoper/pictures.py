import config, json
from utils.helpers.helper_functions import export_to_json


class ShoperPictures:
    def __init__(self, client):
        """Initialize a Shoper Client
        https://developers.shoper.pl/developers/api/resources/product-images
        """
        self.client = client
        self.url = f'{self.client.site_url}/webapi/rest/product-images'

    def create_product_picture(self, image_data: dict):
        """Update a new product image.
        Args:
            image_data (dict): Image data
        Returns:
            bool: True if successful
        """
        self.client._handle_request('POST', self.url, json=image_data)
        return True
    
    def get_product_pictures(self, product_id: int, export: bool = False) -> list:
        """Get product images from Shoper.
        Args:
            product_id (int): Product id
            export (bool): If True, export the product images to a JSON file.
        Returns:
            list: List of product images if successful.
        """
        photo_filter = {
            "filters": json.dumps({"product_id": product_id}),
            "limit": config.SHOPER_LIMIT
        }

        data = self.client._handle_request('GET', self.url, params=photo_filter).json()
        images = data.get('list', [])

        if export:
            export_to_json(images, f'shoper/product_images/shoper_product_images_{product_id}.json')

        return images

    def change_product_picture(self, photo_id: int, new_url: str) -> bool:
        """Changes a current image to a new one
        Args:
            photo_id (int): Shoper current photo id
            photo_url (str): Full new photo url
        Returns:
            True|dict: True if successful, Error dict if failed
        """
        photo_name = new_url.split('/')[-1]
        params = {
            'url': new_url,
            'translations': {'pl_PL': {'name': photo_name}}
        }

        self.client._handle_request('PUT', f'{self.url}/{photo_id}', json=params)
        return True

    def remove_product_picture(self, photo_id: int) -> bool:
        """Removes an image
        Args:
            photo_id (int): Photo id
        Returns:
            True|dict: True if successful, Error dict if failed
        """
        self.client._handle_request('DELETE', f'{self.url}/{photo_id}')
        return True
