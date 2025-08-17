import os
import requests
from pathlib import Path

from loguru import logger
from retry import retry


class StreetViewDownloader:

    def __init__(self, config):
        self.config = config
        self.metadata_url = 'https://maps.googleapis.com/maps/api/streetview/metadata'
        self.image_url = 'https://maps.googleapis.com/maps/api/streetview'


    @retry(tries=2, delay=1, backoff=2, exceptions=(requests.exceptions.RequestException,))
    def StreetViewAvailability(self, lat, lon):
        try:
            params = {
                "location": f"{lat},{lon}",
                "key": self.config.api_key
            }
            response = requests.get(self.metadata_url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('status') == 'OK'

        except requests.exceptions.HTTPError as e:
            logger.error(f"Streetview Metadata API Bad Request Message: {e}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Streetview Metadata API Error at ({lat}, {lon}): {e}")


    @retry(tries=2, delay=1, backoff=2, exceptions=(requests.exceptions.RequestException,))
    def StreetViewImage(self, lat, lon):
        try:
            image_filenames = []
            for heading in self.config.headings:
                params = {
                    "size": self.config.size,
                    "location": f"{lat},{lon}",
                    "fov": self.config.fov,
                    "heading": heading,
                    "pitch": self.config.pitch,
                    "key": self.config.api_key
                }
                response = requests.get(self.image_url, params=params)
                response.raise_for_status()
                lat_str = f"{lat:.4f}".replace("-", "m")  # replace minus with 'm'
                lon_str = f"{lon:.4f}".replace("-", "m")
                heading_str = str(heading)

                filename = f"Street_{lat_str}_{lon_str}_{heading_str}.jpg"
                image_filename = Path(self.config.output_dir) / f"{filename}"

                with open(image_filename, 'wb') as f:
                    f.write(response.content)

                image_filenames.append(str(image_filename))

        except requests.exceptions.HTTPError as e:
            logger.error(f"Streetview API Bad Request Message: {e}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Streetview API Error at ({lat}, {lon}): {e}")
        return image_filenames