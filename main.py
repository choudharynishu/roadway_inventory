import os
import pandas as pd
from dotenv import load_dotenv
from loguru import logger

from src.config import config, settings
from src.ImageExtractor import StreetViewDownloader

def main():
    load_dotenv()
    API_KEY = os.getenv('API_KEY')
    print(API_KEY)

if __name__ == '__main__':
    main()