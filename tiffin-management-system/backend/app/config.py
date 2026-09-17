import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tiffin.db")
APP_NAME = os.getenv("APP_NAME", "Tiffin Management System")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
