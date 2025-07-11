import config
from tqdm import tqdm
from utils.helpers.helper_functions import export_to_json


class ShoperCategories:
    def __init__(self, client):
        """Initialize a Shoper Client
        https://developers.shoper.pl/developers/api/resources/categories
        """
        self.client = client
        self.url = f'{self.client.site_url}/webapi/rest/categories'

    def get_all_categories(self, export: bool = True) -> list[dict]:
        """Get all categories from Shoper.
        Args:
            export (bool): If True, export the categories to a JSON file.
        Returns:
            list: List of categories if successful.
        """
        categories = []
        params = {
            'limit': config.SHOPER_LIMIT,
            'page': 1
        }

        print("ℹ️  Downloading all categories...")
        data = self.client._handle_request('GET', self.url, params=params).json()
        number_of_pages = data['pages']
        categories.extend(data.get('list', []))

        for page in tqdm(range(2, number_of_pages + 1),
                         desc="Downloading pages", unit=" page"):
            
            params['page'] = page
            data = self.client._handle_request('GET', self.url, params=params).json()
            categories.extend(data.get('list', []))

        if export:
            export_to_json(categories, 'shoper/shoper_categories.json')

        return categories
