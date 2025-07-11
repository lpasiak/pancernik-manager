import config
from tqdm import tqdm
from utils.helpers.helper_functions import export_to_json


class ShoperGauges:
    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client
        self.url = f'{self.client.site_url}/webapi/rest/gauges'

    def get_all_gauges(self, export: bool = True) -> list[dict]:
        """Get all Gauges from Shoper.
        Args:
            export (bool): If True, export the gauges to a JSON file.
        Returns:
            list: List of Gauges if successful.
        """
        gauges = []
        params = {
            'limit': config.SHOPER_LIMIT,
            'page': 1
        }

        print("ℹ️  Downloading all gauges...")
        data = self.client._handle_request('GET', self.url, params=params).json()
        number_of_pages = data.get('pages', 1)
        gauges.extend(data.get('list', []))

        for page in tqdm(range(2, number_of_pages + 1),
                         desc="Downloading pages", unit=" page"):
            
            params['page'] = page
            data = self.client._handle_request( 'GET', self.url, params=params).json()
            gauges.extend(data.get('list', []))

        if export:
            export_to_json(gauges, 'shoper/shoper_gauges.json')

        return gauges
