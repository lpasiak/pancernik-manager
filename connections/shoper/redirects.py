import config
from tqdm import tqdm
from utils.helpers.helper_functions import export_to_json


class ShoperRedirects:
    def __init__(self, client):
        """Initialize a Shoper Client
        https://developers.shoper.pl/developers/api/resources/redirects
        """
        self.client = client
        self.url = f'{self.client.site_url}/webapi/rest/redirects'

    def create_redirect(self, redirect_data: dict) -> int:
        """Create a redirect in Shoper.
        Args:
            redirect_data (dict): Data about the redirect:
                route: string
                target: string
        Returns:
            int: Redirect id if succesful
        """
        params = redirect_data
        params['type'] = 0
        redirect_id = self.client._handle_request('POST', self.url, json=params).json()

        return redirect_id
    
    def get_all_redirects(self, export: bool = True) -> list:
        """Get all redirects from Shoper.
        Args:
            export (bool): If True, export the redirects to a JSON file.
        Returns:
            list: List of redirects if successful
        """
        redirects = []
        params = {
            'limit': config.SHOPER_LIMIT,
            'page': 1
        }

        print("ℹ️  Downloading all redirects...")
        data = self.client._handle_request('GET', self.url, params=params).json()
        number_of_pages = data.get('pages', 1)
        redirects.extend(data.get('list', []))

        for page in tqdm(range(2, number_of_pages + 1),
                            desc="Downloading pages", unit=" page"):
            
            params['page'] = page
            data = self.client._handle_request('GET', self.url, params=params).json()
            redirects.extend(data.get('list', []))

        if export:
            export_to_json(redirects, 'shoper/shoper_redirects.json')

        return redirects

    def remove_redirect(self, identifier: str | int) -> bool:
        """Remove a redirect in Shoper.
        Args:
            identifier (str|int): Redirect id
        Returns:
            True|dict: True if succesful, Error dict if failed
        """
        self.client._handle_request('DELETE', f'{self.url}/{identifier}')

        return True
