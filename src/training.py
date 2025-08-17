import os
import shutil

from ultralytics import YOLO

from loguru import logger
from src.config import modelsettings, datasettings
from src.InputData import download_data
from src.processing import preprocessing


def train():
    # Download the open images images
    download_data()
    logger.info(f"Data download complete")
    preprocessing()

    #Instantiate the YOLO model
    model_version = modelsettings.model_version
    model_dir = modelsettings.model_dir
    model = YOLO(os.path.join(model_dir, model_version))
    logger.info(f"Instantiated the YOLO model: {model_version}")

    # Display model information
    model.info()

    # Train the model on the open images, epoch and image sizes
    data_yaml_file = os.path.join(datasettings.train_dir, f"{datasettings.data_yaml}")
    num_epochs = modelsettings.num_epochs
    image_size = modelsettings.image_size
    training_device = modelsettings.device

    results = model.train(data=data_yaml_file, epochs=num_epochs,
                          imgsz=image_size, device=training_device)

    latest_dir = results.save_dir

    #Save the best model
    save_model(latest_dir)
    model = YOLO(os.path.join(modelsettings.best_model_dir, "best.pt"))

    metrics = model.val(data=data_yaml_file)


def save_model(dir):
    best_model_path = f"{dir}/weights/best.pt"
    destinaton_dir = modelsettings.best_model_dir
    os.makedirs(destinaton_dir, exist_ok=True)
    shutil.copy(best_model_path, destinaton_dir)
    logger.info(f'Saving the model from: {best_model_path} '
                f'to directory: {destinaton_dir}')
