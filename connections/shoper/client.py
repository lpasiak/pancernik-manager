import requests, time
import config
from .exceptions import ShoperAPIError


class ShoperAPIClient:
    def __init__(self):
        self.site_url = config.SHOPER_SITE_URL
        self.login = config.SHOPER_LOGIN
        self.password = config.SHOPER_PASSWORD
        self.session = requests.Session()
        self.token = None
        
    def _handle_request(self, method, url, max_retries=5, backoff_factor=1.5, **kwargs):
        """Handle API requests with automatic retry on 429 and 5xx errors."""
        attempt = 0

        while attempt < max_retries:
            response = self.session.request(method, url, **kwargs)

            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 1))
                print(f"429 Too Many Requests. Retrying after {retry_after} seconds...")
                time.sleep(retry_after)
                attempt += 1
                continue

            elif response.status_code in {500, 502, 503, 504}:
                wait = backoff_factor ** attempt
                print(f"{response.status_code} Server Error. Retrying in {wait:.1f} seconds...")
                time.sleep(wait)
                attempt += 1
                continue

            if response.status_code != 200:
                raise ShoperAPIError(response)
            
            return response
            
    def connect(self):
        """Authenticate with the API"""
        response = self._handle_request(
            'POST',
            f'{self.site_url}/webapi/rest/auth',
            auth=(self.login, self.password)
        )

        if response.status_code != 200:
            error_description = response.json().get('error_description', 'Unknown error')
            return {'success': False, 'error': error_description}
        
        self.token = response.json().get('access_token')
        self.session.headers.update({'Authorization': f'Bearer {self.token}'})
        return {'success': True}
    
    @property
    def is_connected(self):
        return self.token is not None