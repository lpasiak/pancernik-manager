import config
from tqdm import tqdm


class ShoperCategories:
    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client

    def get_all_categories(self):
        """Get all categories from Shoper.
        Returns a Data dict if successful, Error dict if failed"""
        categories = []
        url = f'{self.client.site_url}/webapi/rest/categories'
        params = {
            'limit': config.SHOPER_LIMIT,
            'page': 1
        }

        print("ℹ️  Downloading all categories...")
        response = self.client._handle_request('GET', url, params=params)

        if response.status_code != 200:
            error_description = response.json().get('error_description', 'Unknown error')
            return {'success': False, 'error': error_description}

        data = response
        number_of_pages = data['pages']
        categories.extend(data.get('list', []))

        for page in tqdm(range(2, number_of_pages + 1),
                         desc="Downloading pages", unit=" page"):
            
            params['page'] = page
            response = self.client._handle_request('GET', url, params=params)

            if response.status_code != 200:
                error_description = response.json().get('error_description', 'Unknown error')
                return {'success': False, 'error': error_description}

            page_data = response.json().get('list', [])
            categories.extend(page_data)

        return categories
