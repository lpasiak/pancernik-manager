import config
from tqdm import tqdm


class ShoperAttributes:
    def __init__(self, client):
        """Initialize a Shoper Client
        https://developers.shoper.pl/developers/api/resources/attribute-groups
        https://developers.shoper.pl/developers/api/resources/attributes
        """
        self.client = client
        self.url_attribute_groups = f'{self.client.site_url}/webapi/rest/attribute-groups'
        self.url_attributes = f'{self.client.site_url}/webapi/rest/attributes'

    def get_all_attribute_groups(self):
        """Get all attribute groups from Shoper. 
        Returns a Data dict if successful, Error dict if failed"""
        attribute_groups = []
        params = {
            'limit': config.SHOPER_LIMIT,
            'page': 1
        }

        print("ℹ️  Downloading all attribute groups...")
        response = self.client._handle_request(
            'GET',
            self.url_attribute_groups,
            params=params
        )

        if response.status_code != 200:
            error_description = response.json().get('error_description', 'Unknown error')
            return {'success': False, 'error': error_description}

        data = response.json()
        number_of_pages = data.get('pages', 1)
        attribute_groups.extend(data.get('list', []))

        for page in tqdm(range(2, number_of_pages + 1), 
                         desc="Downloading attribute groups", unit=" page"):
            
            params['page'] = page
            response = self.client._handle_request(
                'GET',
                self.url_attribute_groups,
                params=params
            )

            if response.status_code != 200:
                error_description = response.json().get('error_description', 'Unknown error')
                return {'success': False, 'error': error_description}

            page_data = response.json().get('list', [])
            attribute_groups.extend(page_data)

        return attribute_groups

    def get_all_attributes(self):
        """Get all attributes from Shoper. 
        Returns a Data dict if successful, Error dict if failed"""
        attributes = []
        params = {
            'limit': config.SHOPER_LIMIT,
            'page': 1
        }

        print("ℹ️  Downloading all attributes...")
        response = self.client._handle_request(
            'GET',
            self.url_attributes,
            params=params
        )

        if response.status_code != 200:
            error_description = response.json().get('error_description', 'Unknown error')
            return {'success': False, 'error': error_description}

        data = response.json()
        number_of_pages = data.get('pages', 1)
        attributes.extend(data.get('list', []))

        for page in tqdm(range(2, number_of_pages + 1),
                         desc="Downloading pages", unit=" page"):
            
            params['page'] = page
            response = self.client._handle_request(
                'GET',
                self.url_attributes,
                params=params
            )

            if response.status_code != 200:
                error_description = response.json().get('error_description', 'Unknown error')
                return {'success': False, 'error': error_description}

            page_data = response.json().get('list', [])
            attributes.extend(page_data)

        return attributes

    def get_attribute_group_by_id(self, attribute_group_id):
        """Get an attribute group by its ID
        Args:
            attribute_group_id (int): The ID of the attribute group to get
        Returns:
            dict: The attribute group data
        """
        response = self.client._handle_request(
            'GET',
            f'{self.get_all_attribute_groups}/{attribute_group_id}'
        )
        
        if response.status_code != 200:
            error_description = response.json().get('error_description', 'Unknown error')
            return {'success': False, 'error': error_description}
        
        return response.json()

    def update_attribute_group_categories(self, attribute_group_id, categories):
        """Update an attribute group with new categories
        Args:
            attribute_group_id (int): The ID of the attribute group to create
            categories (list): Product categories list as integers
        Returns:
            Error dict if failed, True if succesful
        """
        response = self.client._handle_request(
            'PUT',
            f'{self.url_attribute_groups}/{attribute_group_id}',
            json={'categories': categories}
        )
        
        if response.status_code != 200:
            error_description = response.json().get('error_description', 'Unknown error')
            return {'success': False, 'error': error_description}
        
        return True
