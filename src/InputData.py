import os
import fiftyone as fo

from dotenv import load_dotenv
from loguru import logger

def download_data():
    # setup the download directory
    load_dotenv()
    training_datadir = os.getenv('TRAIN_DIR')
    fo.config.dataset_zoo_dir = training_datadir

    splits = ["train", "validation", "test"]
    dataset = fo.zoo.load_zoo_dataset(
        "open-images-v7",
        splits=splits,
        label_types=["detections"],
        classes=["Traffic light"],
        max_samples=None,
    )
    stats = dataset.stats()
    logger.info(f"Downloaded data for :{splits}, "
                f"Total images downloaded: {stats['samples_count']}, "
                f"Directory address: {training_datadir}")
