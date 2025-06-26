import config
from tqdm import tqdm


class ShoperRedirects:
    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client

    def get_all_redirects(self):
        """Get all redirects from Shoper.
        Returns a Data dict if successful, Error dict if failed"""
        redirects = []
        url = f'{self.client.site_url}/webapi/rest/redirects'
        params = {
            'limit': config.SHOPER_LIMIT,
            'page': 1
        }

        print("ℹ️  Downloading all redirects...")
        response = self.client._handle_request('GET', url, params=params)

        if response.status_code != 200:
            error_description = response.json().get('error_description', 'Unknown error')
            return {'success': False, 'error': error_description}

        data = response.json()
        number_of_pages = data['pages']
        redirects.extend(data.get('list', []))

        for page in tqdm(range(2, number_of_pages + 1),
                            desc="Downloading pages", unit=" page"):
            
            params['page'] = page
            response = self.client._handle_request('GET', url, params=params)

            if response.status_code != 200:
                error_description = response.json().get('error_description', 'Unknown error')
                return {'success': False, 'error': error_description}

            page_data = response.json().get('list', [])
            redirects.extend(page_data)

        return redirects
        
    def create_redirect(self, redirect_data):
        """Create a redirect in Shoper
        Args:
            redirect_data (dict): Data about the redirect:
                redirected_url: string
                target_url: string
        Returns:
            int|dict: Redirect id if succesful, Error dict if failed
        """
        params = {
            'route': redirect_data['redirected_url'],
            'type': 0,
            'target': redirect_data['target_url'],
        }
        
        url = f'{config.SHOPER_SITE_URL}/webapi/rest/redirects'

        response = self.client._handle_request('POST', url, json=params)

        if response.status_code != 200:
            error_description = response.json().get('error_description', 'Unknown error')
            return {'success': False, 'error': error_description}
        
        return response.json()

    def remove_redirect(self, identifier):
        """Remove a redirect
        Args:
            identifier (int): Redirect id
        Returns:
            True|dict: True if succesful, Error dict if failed
        """
        url = f'{config.SHOPER_SITE_URL}/webapi/rest/redirects/{identifier}'
        response = self.client._handle_request('DELETE', url)

        if response.status_code != 200:
            error_description = response.json().get('error_description', 'Unknown error')
            return {'success': False, 'error': error_description}

        return True
