import os
import yaml
import pandas as pd

from loguru import logger
from src.config import datasettings


def preprocessing():
    # List of sets for which the preprocessing needs to happen
    sets = ["train", "validation", "test"]
    try:
        for set in sets:
            logger.info(f"Processing {set}")
            add_annotations(set)
            if set=="train":
                train_img_dir = os.path.join(datasettings.train_dir,"open-images-v7", set, f"images")
            elif set=="validation":
                val_img_dir = os.path.join(datasettings.train_dir,"open-images-v7", set, f"images")

    except Exception as e:
        logger.error(f"Preprocessing failed: {e}")
        raise

    # Create YOLOv5 Dataset Configuration File
    config_file_path = os.path.join(datasettings.train_dir, f"{datasettings.data_yaml}")
    # YOLO Data configuration
    config = {
        'train': train_img_dir,
        'val': val_img_dir,
        'nc': 1,  # Number of classes
        'names': ['Traffic Sign']  # Class Name
    }
    # Save the configuration to a YAML file
    with open(config_file_path, 'w') as file:
        yaml.dump(config, file)

def add_annotations(set):
    logger.info(f"Adding annotations for set: {set}")
    # Directory where train, validation, and test sets are stored
    data_dir = datasettings.train_dir
    # File containing information about each image
    set_label_file = f"detections.csv"

    set_label_dir = os.path.join(data_dir, "open-images-v7", set, "labels")
    set_label_df = pd.read_csv(os.path.join(set_label_dir, set_label_file), header=0)

    # Filter image ids which contain traffic light
    set_label_df = set_label_df[set_label_df['LabelName'] == '/m/015qff']

    class_labels = set_label_df['LabelName'].unique().tolist()
    class_label_map = {label:index for index, label in enumerate(class_labels)}

    set_label_df['class_id'] = set_label_df['LabelName'].map(class_label_map)
    set_label_df['x_center'] = (set_label_df['XMin'] + set_label_df['XMax']) * 0.5
    set_label_df['y_center'] = (set_label_df['YMin'] + set_label_df['YMax']) * 0.5
    set_label_df['width'] = abs(set_label_df['XMax'] - set_label_df['XMin'])
    set_label_df['height'] = abs(set_label_df['YMax'] - set_label_df['YMin'])
    set_label_df['yolo_line'] = set_label_df.apply(
            lambda r: f"{r['class_id']} {r['x_center']:.6f} {r['y_center']:.6f} {r['width']:.6f} {r['height']:.6f}",
            axis=1
        )
    grouped_df = set_label_df.groupby('ImageID')['yolo_line']
    for image_id, annotations in grouped_df:
        filename = os.path.join(set_label_dir, f"{image_id}.txt")
        if os.path.exists(filename):
            logger.info(f"Skipping {filename}, already exists.")
            continue
        with open(filename, 'w') as f:
            logger.info(f"Creating {filename}")
            f.write('\n'.join(annotations.values) + '\n')
    logger.info(f"Completed annotations for set: {set}")
