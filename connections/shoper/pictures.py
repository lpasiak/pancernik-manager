import config, json


class ShoperPictures:
    def __init__(self, client):
        """Initialize a Shoper Client
        https://developers.shoper.pl/developers/api/resources/product-images
        """
        self.client = client
        self.url = f'{self.client.site_url}/webapi/rest/product-images'

    def get_product_pictures(self, product_id):
        """Get product images from Shoper
        Args:
            product_id (int): Product id
        Returns:
            list|dict: List of product images if successful, Error dict or empty list if failed
        """
        photo_filter = {
            "filters": json.dumps({"product_id": product_id}),
            "limit": config.SHOPER_LIMIT
        }

        response = self.client._handle_request(
            'GET',
            self.url,
            params=photo_filter
            )

        if response.status_code != 200:
            error_description = response.json().get('error_description', 'Unknown error')
            return {'success': False, 'error': error_description}
        
        return response.json()['list']
        
    def update_product_image(self, image_data):
        """Update product image
        Args:
            image_data (dict): Image data
        Returns:
            dict: Image data if successful, Error dict if failed
        """
        response = self.client._handle_request(
            'POST',
            self.url,
            json=image_data
        )
        
        if response.status_code != 200:
            error_description = response.json().get('error_description', 'Unknown error')
            return {'success': False, 'error': error_description}
        
        return response.json()

    def change_product_picture(self, photo_id, new_url):
        """Changes a photo to a new one
        Args:
            photo_id (int): Photo id
            photo_url (str): Full photo url
        Returns:
            True|dict: True if successful, Error dict if failed
        """
        photo_name = new_url.split('/')[-1]

        params = {
            'url': new_url,
            'translations': {'pl_PL': {'name': photo_name}}
        }
        response = self.client._handle_request(
            'PUT',
            f'{self.url}/{photo_id}',
            json=params
        )
        
        if response.status_code != 200:
            error_description = response.json().get('error_description', 'Unknown error')
            return {'success': False, 'error': error_description}
        
        return True

    def remove_product_image(self, photo_id):
        """Removes a photo
        Args:
            photo_id (int): Photo id
        Returns:
            True|dict: True if successful, Error dict if failed
        """

        response = self.client._handle_request(
            'DELETE',
            f'{self.url}/{photo_id}'
        )
        
        if response.status_code != 200:
            error_description = response.json().get('error_description', 'Unknown error')
            return {'success': False, 'error': error_description}
        
        return True