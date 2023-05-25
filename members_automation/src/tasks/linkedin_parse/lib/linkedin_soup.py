import logging
from datetime import datetime
import src.tasks.linkedin_parse.lib.commons as commons
from typing import Dict, Tuple
import urllib.request
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
import requests
from typing import List
from serpapi import GoogleSearch
import pandas as pd
from src.utils.chrome import Sleep

log = logging.getLogger(__name__)


def parse_profile_multiple(
        df_profiles: pd.DataFrame,
        nubela_api_key: str,
        serapi_api_key: str
):
    dict_pictures = {}
    list_users = list()
    df_exceptions = pd.DataFrame(columns=["Name", "error"])
    date_today = datetime.now().strftime("%Y-%m-%d")

    for profile in df_profiles.itertuples():

        dict_profile = profile._asdict()
        dict_profile.pop("Index")
        profile_name = profile.Name
        profile_url = profile.LinkedIn

        log.info(f"Parsing {profile_name}: Start")
        picfile = commons.get_picfile_name(profile_name)
        try:
            current_role, profile_picture = parse_profile_single(
                profile_url,
                nubela_api_key,
                serapi_api_key)

            dict_pictures[profile_name] = {
                "picture_data": profile_picture,
                "picfile": picfile}

            dict_profile["Title"] = current_role
            dict_profile["last_updated"] = date_today
            list_users.append(dict_profile)
        except Exception as e:
            log.info("Unauthorized")
            df_exceptions = df_exceptions.append({"Name": profile_name, "error": str(e)}, ignore_index=True)
        log.info(f"Parsing {profile_name}: End")

    df_team_parsed = pd.DataFrame(list_users)
    return df_team_parsed, dict_pictures, df_exceptions


def parse_profile_single(
        profile_url: str,
        nubela_api_key,
        serapi_api_key) -> Tuple[str, bytes]:
    # "https://proxy.scrapeops.io/v1/?api_key=912a36cb-f7af-4563-ada0-0d6147802579&url=https://www.linkedin.com/in/david-bofill-pages/"

    #html_doc = download_html(profile_url, proxy_url, list_scrapeops_api_keys)

    #html_soup = BeautifulSoup(html_doc, features="lxml")
    Sleep.long()
    current_role = get_role_from_google(profile_url, serapi_api_key)
    log.debug("Parsed current role")

    profile_picture = get_profile_picture(profile_url, nubela_api_key)
    log.debug("Downloaded profile picture")

    return current_role, profile_picture


def download_html(profile_url, proxy_url, list_proxy_api_keys: str):
    success = 0
    for api_key in list_proxy_api_keys:
        request_url = f"{proxy_url}?api_key={api_key}&url={profile_url}"
        log.info(f"Trying url: {request_url}")
        try:
            website = urllib.request.urlopen(request_url)
            mybytes = website.read()
            website.close()
            html_doc = mybytes.decode("utf8")
            log.info("Success!")
            success = 1
        except Exception as e:
            log.warning("API Key has been overused, trying a different one")
        if success == 1:
            return html_doc

    return Exception("There are no proxy API keys left")


def get_role_from_html(html_soup):
    current_role = html_soup.find("h2", attrs={"class": "top-card-layout__headline"}).get_text(strip=True)
    return current_role


def get_profile_picture(profile_url, nubela_api_key):
    api_endpoint = "https://nubela.co/proxycurl/api/linkedin/person/profile-picture"
    header_dic = {"Authorization": "Bearer " + nubela_api_key}
    params = {"linkedin_person_profile_url": profile_url}
    response = requests.get(api_endpoint, params=params, headers=header_dic)
    pic_url = response.json()["tmp_profile_pic_url"]
    image_data = requests.get(pic_url).content
    return image_data


def get_role_from_google(profile_url, serapi_api_key):
    params = {
        "engine": "google",
        "q": profile_url,
        "hl": "en",
        "gl": "es",
        "api_key": serapi_api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    for result in results["organic_results"]:
        current_role = result["title"]
        result_link = result["link"]
        if get_url_tail(result_link) == get_url_tail(profile_url):
            return current_role
    raise Exception(f"Profile not found for url {profile_url}")


def get_url_tail(url):
    split_result = urlsplit(url)
    path = split_result.path.rstrip("/")
    tail = path.split("/")[-1]
    return tail
