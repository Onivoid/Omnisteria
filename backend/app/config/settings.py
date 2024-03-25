import os
from dotenv import load_dotenv

load_dotenv('../config/.env')

DATABASE_URL = os.getenv('DATABASE_URL')