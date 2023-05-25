import logging
from urllib.parse import urljoin, urlsplit

import requests

log = logging.getLogger(__name__)


def get_picfile_name(name):
    picfile = name.replace(" ", "-")
    return picfile


def clean_current_role(current_role):
    current_role = current_role.replace("@", "at")
    current_role = current_role.capitalize()
    return current_role


def download_profile_picture(profile_picture_url):
    profile_picture_data = requests.get(profile_picture_url).content
    return profile_picture_data
