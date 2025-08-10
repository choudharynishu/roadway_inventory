import os
import pandas as pd
from dotenv import load_dotenv
from loguru import logger

from src.config import Config
from src.InferenceImageExtractor import StreetViewDownloader
from src.training import train
from src.processing import preprocessing

def main():
    load_dotenv()
    config = Config(
        size = "640x640",
        fov= 90,
        headings = [0, 90, 180, 270],
        pitch= 0,
        api_key = os.getenv('API_KEY'),
        output_dir = r"data/streetview"
    )
    #downloader = StreetViewDownloader(config)
    #downloader.StreetViewImage(30.407820, -97.715878)
    preprocessing()
    #train()


if __name__ == '__main__':
    main()
