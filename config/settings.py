from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
import os

# All the directories necesarry for the project
ROOT_DIR = Path(__file__).parent.parent
ENVDIR = ROOT_DIR / 'credentials' / '.env'
DATA_DIR = ROOT_DIR / 'data'
MANAGERS_DIR = ROOT_DIR / 'managers'
EXPORTS_DIR = ROOT_DIR / 'exports'
LOGGING_DIR = ROOT_DIR / 'logging'

DRIVE_EXPORT_DIR = r'H:\Pansernik\Eksporty' if os.path.exists('H:') else None

# Load environment variables from the .env file
load_dotenv(ENVDIR)

# API Connections, E-commerce platforms, marketplaces, etc.
SHOPER_SITE = 'MAIN' # TEST (development) or MAIN (deployment)
SHOPER_SITE_URL = os.getenv(f'SHOPER_SITE_URL_{SHOPER_SITE}')
SHOPER_LOGIN = os.getenv(f'SHOPER_LOGIN_{SHOPER_SITE}')
SHOPER_PASSWORD = os.getenv(f'SHOPER_PASSWORD_{SHOPER_SITE}')
SHOPER_LIMIT = 50

SHOPIFY_CREDENTIALS = {
    'api_key': os.getenv('SHOPIFY_API_KEY'),
    'api_secret': os.getenv('SHOPIFY_API_SECRET'),
    'api_token': os.getenv('SHOPIFY_API_TOKEN'),
    'shop_url': os.getenv('SHOPIFY_URL')
}
SHOPIFY_API_VERSION = '2025-04'

IDOSELL_BIZON_RETAIL_SITE = os.getenv('IDOSELL_RETAIL_SITE')
IDOSELL_BIZON_B2B_SITE = os.getenv('IDOSELL_B2B_SITE')
IDOSELL_API_KEY = os.getenv('IDOSELL_API_KEY')
IDOSELL_API_VERSION = 'v5'

ALLEGRO_SITE = 'MAIN' # SANDBOX (development) or MAIN (deployment)
ALLEGRO_API_SECRET = os.getenv(f'ALLEGRO_API_SECRET_{ALLEGRO_SITE}')
ALLEGRO_CLIENT_ID = os.getenv(f'ALLEGRO_CLIENT_ID_{ALLEGRO_SITE}')
ALLEGRO_API_URL = os.getenv(f'ALLEGRO_API_URL_{ALLEGRO_SITE}')
ALLEGRO_API_VERSION = 'application/vnd.allegro.public.v1+json'

EBAY_CLIENT_ID = os.getenv('EBAY_CLIENT_ID')
EBAY_CLIENT_SECRET = os.getenv('EBAY_CLIENT_SECRET')
EBAY_DEV_ID = os.getenv('EBAY_DEV_ID')
EBAY_REDIRECT_URI = os.getenv('EBAY_REDIRECT_URI')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

EASYSTORAGE_URL = os.getenv('EASYSTORAGE_URL')
SUBIEKT_URL = os.getenv('SUBIEKT_URL')
DOMAIN_CREDENTIALS = {
    'username': os.getenv('DOMAIN_LOGIN'),
    'password': os.getenv('DOMAIN_PASSWORD')
}

GOOGLE_CREDENTIALS_FILE = ROOT_DIR / 'credentials' / 'gsheets_credentials.json'

# GOOGLE_SHEET_IDS
BIZON_SHEET_ID = os.getenv('BIZON_SHEET_ID')
BIZON_PRODUCT_INFO = 'Informacja produktowa'

PRICES_SHEET_FOR_COGS_ID = os.getenv('PRICES_SHEET_FOR_COGS_ID')

PROMO_SHEET_ID = os.getenv('PROMO_SHEET_ID')
PROMO_SHEET_EXPORT_NAME = 'Eksport'
PROMO_SHEET_IMPORT_NAME_PERCENT = 'Do importu procenty'
PROMO_SHEET_KUBA = 'KubaBuba'
PROMO_SHEET_TO_REMOVE = 'Do usunięcia'

ALLEGRO_PROMO_SHEET_ID = os.getenv('ALLEGRO_PROMO_SHEET_ID')
ALLEGRO_PROMO_SHEET_NAME = 'Allegro'
ALLEGRO_PROMO_SHEET_HELPER_NAME = 'Allegro Promocje'

OUTLET_SHEET_ID = os.getenv('OUTLET_SHEET_ID')
OUTLET_SHEET_NAME = 'Outlety'
OUTLET_SHEET_LACKING_PRODUCTS_NAME = 'Brak produktów'
OUTLET_SHEET_ARCHIVED_NAME = 'Archiwum'

CLEANUP_SHEET_ID = os.getenv('CLEANUP_SHEET_ID')
CLEANUP_SHEET_DIMENSIONS_NAME = 'Wymiary'
CLEANUP_SHEET_DIMENSIONS_IGNORE_NAME = 'Bez wymiarów'
CLEANUP_ALLEGRO_TITLES_NAME = 'Nazwy Allegro'
MISSING_ALLEGRO_OFFERS_NAME = 'Uzupełnianie Allegro | sklep-pancernik'
MISSING_SHOPIFY_OFFERS_NAME = 'Uzupełnianie Shopify'
MISSING_ATTRIBUTES_NAME = 'Uzupełnianie Atrybuty'
CLEANUP_ARCHIVED_NAME = 'Archiwum'

BUNDLE_SHEET_ID = '15azOFBzVc4OrtI1HJ2qNWiDOi35hFLEwOTrnYZIe16w'
BUNDLE_SHEET_NAME = 'do wystawienia'

# FIXED VARIABLES
GOOGLE_EMAIL_SENDER = os.getenv('GOOGLE_EMAIL_SENDER')
GOOGLE_EMAIL_PASSWORD = os.getenv('GOOGLE_EMAIL_PASSWORD')

TODAY = datetime.today().strftime('%d-%m-%Y')
TODAY_PD = pd.Timestamp.today()

OUTLET_MAIL_RECIPIENTS = os.getenv('OUTLET_MAIL_RECIPIENTS')
OUTLET_MAIL_RECIPIENT_LIST = [email.strip() for email in OUTLET_MAIL_RECIPIENTS.split(',') if email.strip()]

PROMO_MAIL_RECIPIENTS = os.getenv('PROMO_MAIL_RECIPIENTS')
PROMO_MAIL_RECIPIENT_LIST = [email.strip() for email in PROMO_MAIL_RECIPIENTS.split(',') if email.strip()]

PROMO_TIME_END = '2031-12-31'

REDIRECT_TARGET_OUTLET_URL = '/outlet'

OUTLET_VALID_DAMAGE_TYPES = ['USZ', 'ZAR', 'OBA']
OUTLET_DISCOUNT_PERCENTAGE = 20
OUTLET_DAYS_TO_DISCOUNT = 14
OUTLET_DAYS_TO_BE_REMOVED = 60
OUTLET_REDIRECT_DAYS_TO_BE_REMOVED = 21

OUTLET_ATTRIBUTE = {
    'id': '1402',
    'group': '577'
}
PRODUCT_TYPE = {
    'id': '1370',
    'group': '550',
}
COST_OF_GOODS_SOLD = {
    'id': '1686',
    'group': '550'
}
PRODUCER_SERIES = {
    'id': '1160',
    'group': '550'
}
