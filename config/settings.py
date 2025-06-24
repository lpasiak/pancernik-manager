from pathlib import Path
from dotenv import load_dotenv

# All the directories necesarry for the project
ROOT_DIR = Path(__file__).parent.parent
ENVDIR = ROOT_DIR / 'credentials' / '.env'
DATA_DIR = ROOT_DIR / 'data'
EXPORTS_DIR = ROOT_DIR / 'exports'

# Load environment variables from the .env file
load_dotenv(ENVDIR)
