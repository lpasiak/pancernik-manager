
class ShoperAPIError(Exception):
    def __init__(self, response):
        self.status_code = response.status_code
        self.url = response.url

        try:
            self.error_data = response.json()
        except Exception:
            self.error_data = {}

        self.error = self.error_data.get('error', 'Unknown_error')
        self.message = self.error_data.get('error_description', response.text)

        # Final exception message
        super().__init__(f"[{self.status_code}] {self.error}: {self.message} ({self.url})")
