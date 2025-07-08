import config
import json
from tqdm import tqdm


class AllegroOffers:
    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client

    def get_an_offer_by_id(self, identifier):
        """Get an offer by its ID from Allegro API.
        Args:
            identifier (str): The ID of the offer to retrieve.
        Returns:
            dict: The offer data if successful, or an Error Dict if failed.

        https://developer.allegro.pl/documentation#tag/User's-offer-information/operation/getProductOffer
        """
        url = f'{config.ALLEGRO_API_URL}/sale/product-offers/{identifier}'
        response = self.client.session.request('GET', url)
        response_json = response.json()

        if response.status_code != 200:
            if 'errors' in response_json and isinstance(response_json['errors'], list):
                error_message = response_json['errors'][0].get('message', 'Unknown error')
            else:
                error_message = response_json.get('error_description', 'Unknown error')

            return {'success': False, 'error': error_message}
        
        return response.json()
    
    def update_an_offer_by_id(self, identifier, data):
        """Update an offer by its ID in Allegro API.
        Args:
            identifier (str): The ID of the offer to update.
            data (dict): The data to update the offer with.
        Returns:
            dict: The updated offer data if successful, or an Error Dict if failed.

        https://developer.allegro.pl/documentation#tag/Offer-management/operation/editProductOffers
        """
        url = f'{config.ALLEGRO_API_URL}/sale/product-offers/{identifier}'
        headers = {'Accept-Language': 'pl-PL', 'Content-Type': 'application/vnd.allegro.public.v1+json'}

        response = self.client.session.request('PATCH', url, headers=headers, json=data)
        response_json = response.json()

        if response.status_code != 200:
            if 'errors' in response_json and isinstance(response_json['errors'], list):
                error_message = response_json['errors'][0].get('message', 'Unknown error')
            else:
                error_message = response_json.get('error_description', 'Unknown error')

            return {'success': False, 'error': error_message}
        
        return response.json()

    def get_all_offers(self):
        """Get all offers from Allegro API.
        Returns:
            list: A list of all offers if successful, or an Error Dict if failed.

        https://developer.allegro.pl/documentation#tag/User's-offer-information/operation/searchOffersUsingGET
        """
        url = f'{config.ALLEGRO_API_URL}/sale/offers'
        all_offers = []

        params = {'limit': 100, 'offset': 0}

        response = self.client.session.request('GET', url, params=params)
        response_json = response.json()

        if response.status_code != 200:
            if 'errors' in response_json and isinstance(response_json['errors'], list):
                error_message = response_json['errors'][0].get('message', 'Unknown error')
            else:
                error_message = response_json.get('error_description', 'Unknown error')

            return {'success': False, 'error': error_message}
        
        data = response.json()
        total_products = data.get('totalCount', 0)

        for offset in tqdm(range(0, total_products, 100),
                        desc="Downloading offers", unit=" product"):
            
            params['offset'] = offset
            response = self.client.session.request('GET', url, params=params)
            response_json = response.json()

            if response.status_code != 200:
                if 'errors' in response_json and isinstance(response_json['errors'], list):
                    error_message = response_json['errors'][0].get('message', 'Unknown error')
                else:
                    error_message = response_json.get('error_description', 'Unknown error')

                return {'success': False, 'error': error_message}
            
            offers = response_json.get('offers', [])

            if not offers:
                break

            all_offers.extend(offers)

        with open('allegro.json', 'w', encoding='utf-8') as f:
            json.dump(all_offers, f, indent=2, ensure_ascii=False)

        return all_offers
