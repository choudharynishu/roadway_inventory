import os
import pandas as pd
from dotenv import load_dotenv
from loguru import logger
from ultralytics import YOLO

from src.config import Config, datasettings, modelsettings
from src.InferenceImageExtractor import StreetViewDownloader
from src.training import train


def load_model():
    model_dir = modelsettings.best_model_dir
    model_filepath = os.path.join(model_dir, "best.pt")
    if not os.path.isfile(model_filepath):
        logger.info(f"The trained model doesnt exist, training..")
        train()
        logger.info(f"Loading trained model..")
    return model_filepath


def check_image(image_filename, model):
    results = model.predict(image_filename, save=False, verbose=False)
    classes = results[0].boxes.cls.tolist()
    return 0 in classes


def process_inference_data(dataframe, downloader):
    model = YOLO(load_model())
    for index, row in dataframe.iterrows():
        lat, lon = row['Latitude'], row['Longitude']

        if downloader.StreetViewAvailability(lat, lon):
            image_filenames = downloader.StreetViewImage(lat, lon)
            traffic_control_list = [check_image(image_file, model) for image_file in image_filenames]

            if any(traffic_control_list):
                dataframe.loc[index, 'traffic_control']='signalized'
            else:
                dataframe.loc[index, 'traffic_control']='stop_controlled'
        else:
            dataframe.loc[index, 'traffic_control']='streetview_unavailable'


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

    downloader = StreetViewDownloader(config)
    inference_df = pd.read_excel(os.path.join("data", datasettings.inference_filename), header=0, nrows=50)

    process_inference_data(inference_df, downloader)
    inference_df.to_csv(os.path.join("data", "Inference_results.csv"), index=False)


if __name__ == '__main__':
    main()
