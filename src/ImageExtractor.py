import os
import requests
import logger
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
        headings = [0, 90, 180, 270]
        try:
            for heading in headings:
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

                with open(os.path.join(self.config.output_dir, f"Street_{lat}_{lon}_{heading}.jpg"), 'wb') as f:
                    f.write(response.content)

        except requests.exceptions.HTTPError as e:
            logger.error(f"Streetview API Bad Request Message: {e}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Streetview API Error at ({lat}, {lon}): {e}")
