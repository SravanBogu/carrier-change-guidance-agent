import os

from dotenv import load_dotenv


load_dotenv()


CARRIER_INTELLIGENCE_API_BASE_URL = os.getenv(
    "CARRIER_INTELLIGENCE_API_BASE_URL",
    "http://127.0.0.1:8000",
).rstrip("/")