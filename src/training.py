import os

from dotenv import load_dotenv
from ultralytics import YOLO

from loguru import logger
from src.config import modelsettings
from src.InputData import download_data


def train():
    # Download the open images data
    #download_data()
    logger.info(f"Data download complete")

    # Data Processing


    #Instantiate the YOLO model
    model_version = modelsettings.model_version
    model_dir = modelsettings.model_dir
    model = YOLO(os.path.join(model_dir, model_version))
    logger.info(f"Instantiated the YOLO model: {model_version}")

    # Display model information
    model.info()

    # Train the model on the open images data, epoch and image sizes
    # results = model.train(data="coco8.yaml", epochs=100, imgsz=640)
