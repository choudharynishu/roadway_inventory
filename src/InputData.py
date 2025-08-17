import os
import fiftyone as fo

from loguru import logger
from src.config import datasettings


def download_data():
    training_datadir = datasettings.train_dir
    fo.config.dataset_zoo_dir = training_datadir

    splits = ["train", "validation", "test"]
    dataset = fo.zoo.load_zoo_dataset(
        "open-images-v7",
        splits=splits,
        label_types=["detections"],
        classes=["Traffic light"],
        max_samples=None,
    )
    original_dirname = [os.path.join(training_datadir,"open-images-v7", split, "data" ) for split in splits]
    yolo_dirname = [os.path.join(training_datadir,"open-images-v7", split, "images" ) for split in splits]

    for orig, yolo in zip(original_dirname, yolo_dirname):
        rename_directories(orig, yolo)

    stats = dataset.stats()
    logger.info(f"Downloaded data for :{splits}, "
                f"Total images downloaded: {stats['samples_count']}, "
                f"Directory address: {training_datadir}")

def rename_directories(old, new):
    logger.info(f"Renaming file: {old}")
    if os.path.isdir(old):
        os.rename(old, new)
    else:
        print(f"Directory {old} doesnt exist")
        logger.error(f"Directory {old} doesnt exist")