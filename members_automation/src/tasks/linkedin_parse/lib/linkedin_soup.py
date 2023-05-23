import logging
from datetime import datetime
import src.tasks.linkedin_parse.lib.commons as commons
from typing import Dict, Tuple
import urllib.request
from bs4 import BeautifulSoup
import requests
from typing import List

import pandas as pd

log = logging.getLogger(__name__)


def parse_profile_multiple(df_profiles: pd.DataFrame, proxy_url: str, list_proxy_api_keys: List[str]):
    dict_pictures = {}
    list_users = list()
    df_exceptions = pd.DataFrame(columns=["name", "error"])
    date_today = datetime.now().strftime("%Y-%m-%d")

    for profile in df_profiles.itertuples():

        dict_profile = profile._asdict()
        dict_profile.pop("Index")
        profile_name = profile.name
        profile_url = commons.normalize_url(profile.linkedin)

        log.info(f"Parsing {profile_name}: Start")
        try:
            picfile = commons.get_picfile_name(profile_url)
            current_role, profile_picture = parse_profile_single(profile_url, proxy_url, list_proxy_api_keys)

            dict_pictures[profile_name] = {
                "picture_data": profile_picture,
                "picfile": picfile}

            dict_profile["title"] = current_role
            dict_profile["last_updated"] = date_today
            list_users.append(dict_profile)
        except Exception as e:
            log.info("Unauthorized")
            df_exceptions = df_exceptions.append({"name": profile_name, "error": str(e)}, ignore_index=True)
        log.info(f"Parsing {profile_name}: End")

    df_team_parsed = pd.DataFrame(list_users)
    return df_team_parsed, dict_pictures, df_exceptions


def parse_profile_single(profile_url: str, proxy_url: str, list_proxy_api_keys: List[str]) -> Tuple[str, bytes]:
    # "https://proxy.scrapeops.io/v1/?api_key=912a36cb-f7af-4563-ada0-0d6147802579&url=https://www.linkedin.com/in/david-bofill-pages/"

    html_doc = download_html(profile_url, proxy_url, list_proxy_api_keys)
    log.debug("Adquired html")

    html_soup = BeautifulSoup(html_doc, features="lxml")

    current_role = get_current_role(html_soup)
    log.debug("Parsed current role")

    profile_picture = get_profile_picture(html_soup)
    log.debug("Downloaded profile picture")

    return current_role, profile_picture


def download_html(profile_url, proxy_url, list_proxy_api_keys: str):
    success = 0
    for api_key in list_proxy_api_keys:
        try:
            request_url = f"{proxy_url}?api_key={api_key}&url={profile_url}"
            website = urllib.request.urlopen(request_url)
            mybytes = website.read()
            html_doc = mybytes.decode("utf8")
            website.close()
            success = 1
        except Exception as e:
            log.warning("API Key has been overused, trying a different one")
    if success == 0:
        raise Exception("There are no proxy API keys left")
    return html_doc


def get_current_role(html_soup):
    current_role = html_soup.find("h2").get_text(strip=True)
    return current_role


def get_profile_picture(html_soup):
    image_data = requests.get(html_soup.find("meta", property="og:image")["content"]).content
    return image_data
