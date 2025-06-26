import config
from tqdm import tqdm


class ShoperGauges:
    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client
        self.url = f'{self.client.site_url}/webapi/rest/gauges'

    def get_all_gauges(self):
        """Get all gauges from Shoper.
        Returns a Data list if successful, Error dict if failed"""
        gauges = []
        params = {
            'limit': config.SHOPER_LIMIT,
            'page': 1
        }

        print("ℹ️  Downloading all gauges...")
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
        gauges.extend(data.get('list', []))

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

            gauges.extend(response.json().get('list', []))

        return gauges
