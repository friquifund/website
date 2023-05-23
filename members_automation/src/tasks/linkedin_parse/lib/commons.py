import logging
from urllib.parse import urljoin, urlsplit

import requests

log = logging.getLogger(__name__)


def get_picfile_name(url):
    picfile = url.replace("https://www.linkedin.com/in/", "")
    picfile = picfile.replace("/", "")
    picfile = f"{picfile}.jpeg"
    return picfile


def clean_current_role(current_role):
    current_role = current_role.replace("@", "at")
    current_role = current_role.capitalize()
    return current_role


def download_profile_picture(profile_picture_url):
    profile_picture_data = requests.get(profile_picture_url).content
    return profile_picture_data


def normalize_url(url):
    # Clean the URL by adding "https://" if missing
    if not url.startswith("http"):
        url = "https://" + url

    # Normalize the URL to remove any extraneous components
    parsed_url = urlsplit(url)
    normalized_url = urljoin(parsed_url.scheme + "://" + parsed_url.netloc, parsed_url.path)
    normalized_url = normalized_url.replace(" ", "")
    normalized_url = normalized_url.replace("https://es.linkedin.com", "https://www.linkedin.com")
    normalized_url = normalized_url.replace("https://linkedin.com", "https://www.linkedin.com")
    return normalized_url
