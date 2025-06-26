import requests, time
import config


class ShoperAPIClient:
    def __init__(self):
        self.site_url = config.SHOPER_SITE_URL
        self.login = config.SHOPER_LOGIN
        self.password = config.SHOPER_PASSWORD
        self.session = requests.Session()
        self.token = None
        
    def _handle_request(self, method, url, **kwargs):
        """Handle API requests with automatic retry on 429 errors."""
        while True:
            response = self.session.request(method, url, **kwargs)

            if response.status_code == 429:  # Too Many Requests - rate limit exceeded
                retry_after = int(response.headers.get('Retry-After', 1))
                time.sleep(retry_after)
            else:
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
        
    @property
    def is_connected(self):
        return self.token is not None