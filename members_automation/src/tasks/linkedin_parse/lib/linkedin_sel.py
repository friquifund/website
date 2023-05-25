from typing import Dict, Tuple, List
import logging
import pandas as pd
import requests
from selenium.webdriver.common.by import By
from urllib.parse import urljoin, urlsplit
from datetime import datetime
import src.tasks.linkedin_parse.lib.commons as commons

from src.utils.chrome import Sleep, get_driver, kill_driver

log = logging.getLogger(__name__)


class Linkedin:
    def __init__(self, username, password, html_structure):
        self.username = username
        self.password = password
        self.html_structure = html_structure
        self.driver = get_driver()
        self.driver.get("https://www.linkedin.com/login")
        Sleep.med()

    def login(self):

        if self.element_exists(self.html_structure.login.cookies):
            try:
                self.driver.find_element(By.XPATH, self.html_structure.login.cookies).click()
                Sleep.med()
            except Exception as e:
                log.warning(e)
        if self.element_exists(self.html_structure.login.user):
            self.driver.find_element(By.XPATH, self.html_structure.login.user).send_keys(self.username)
            self.driver.find_element(By.XPATH, self.html_structure.login.password).send_keys(self.password)
            self.driver.find_element(By.XPATH, self.html_structure.login.click).click()
            Sleep.med()
        if self.element_exists(self.html_structure.profile_setup.phone_number):
            self.driver.find_element(By.XPATH, self.html_structure.profile_setup.click).click()
            Sleep.med()
        if self.element_exists(self.html_structure.profile_setup.cookies):
            self.driver.find_element(By.XPATH, self.html_structure.profile_setup.cookies).click()
            Sleep.med()

    def parse_profile_multiple(self, df_eligible: pd.DataFrame) -> Tuple[pd.DataFrame, Dict, pd.DataFrame]:
        dict_pictures = {}
        list_users = list()
        df_exceptions = pd.DataFrame(columns=["Name", "error"])
        date_today = datetime.now().strftime("%Y-%m-%d")

        for profile in df_eligible.itertuples():
            dict_profile = profile._asdict()
            dict_profile.pop("Index")
            profile_url = profile.LinkedIn
            profile_name = profile.Name
            log.info(f"Parsing {profile_name}: Start")
            picfile = commons.get_picfile_name(profile_url)
            try:

                current_role, profile_picture = self.parse_profile_single(profile_url)
                dict_profile["Title"] = current_role
                dict_profile["last_updated"] = date_today

                dict_pictures[profile_name] = {
                    "picture_data": self.download_profile_picture(),
                    "picfile": picfile}

            except Exception as e:
                df_exceptions = df_exceptions.append({"Name": profile_name, "error": str(e)}, ignore_index=True)
            log.info(f"Parsing {profile_name}: End")

        df_team = pd.DataFrame(list_users)
        return df_team, dict_pictures, df_exceptions

    def parse_profile_single(self, url: str) -> pd.DataFrame:

        self.driver.get(url)
        log.info(f"URL {url} loaded")
        Sleep.extra_long()

        current_role = self.get_current_role()
        log.debug(f"Role {current_role} parsed")

        profile_picture = self.download_profile_picture()
        log.debug("Downloaded profile picture")

        return current_role, profile_picture

    @staticmethod
    def get_picfile_name(url):
        picfile = url.replace("https://www.linkedin.com/in/", "")
        picfile = picfile.replace("/", "")
        picfile = f"{picfile}.jpeg"
        return picfile

    def get_current_role(self):
        role_element = self.choose_element(self.html_structure.profile.current_role)
        current_role = self.driver.find_element(By.XPATH, role_element).text
        current_role = current_role.replace("@", "at")
        current_role = current_role.capitalize()
        return current_role

    def download_profile_picture(self):
        picture_element = self.choose_element(self.html_structure.profile.picture)
        profile_picture_url = self.driver.find_element(By.XPATH, picture_element).get_attribute("src")
        profile_picture_data = requests.get(profile_picture_url).content
        Sleep.med()
        log.info("Picfile parsed")
        return profile_picture_data

    @staticmethod
    def save_profile_picture(self, profile_picture, filepath):
        with open(filepath, "wb") as handler:
            handler.write(profile_picture)

    @staticmethod
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

    def element_exists(self, html_element):
        return len(list(self.driver.find_elements(By.XPATH, html_element))) > 0

    def choose_element(self, list_html_element: List[str]):
        if not isinstance(list_html_element, list):
            return list_html_element
        for html_element in list_html_element:
            if self.element_exists(html_element):
                return html_element

    def end_session(self):
        self.driver.stop_client()
        kill_driver()
