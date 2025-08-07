import os
import fiftyone as fo

from dotenv import load_dotenv


def download_data():
    # setup the download directory
    load_dotenv()
    fo.config.dataset_zoo_dir = os.getenv('TRAIN_DIR')

    splits = ["train", "validation", "test"]
    dataset = fo.zoo.load_zoo_dataset(
        "open-images-v7",
        splits=splits,
        label_types=["detections"],
        classes=["Traffic light"],
        max_samples=None,
    )
