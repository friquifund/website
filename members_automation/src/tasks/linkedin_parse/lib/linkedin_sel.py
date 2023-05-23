from typing import Dict, Tuple, List
import logging
import pandas as pd
import requests
from selenium.webdriver.common.by import By
from urllib.parse import urljoin, urlsplit
from datetime import datetime

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
            self.driver.find_element(By.XPATH, self.html_structure.login.cookies).click()
            Sleep.med()
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
        df_exceptions = pd.DataFrame(columns=["name", "error"])
        date_today = datetime.now().strftime("%Y-%m-%d")

        for _, profile in df_eligible.iterrows():
            profile_url = profile["linkedin"]
            profile_name = profile["name"]
            log.info(f"Parsing {profile_name}: Start")
            try:
                df_profile = self.parse_profile(profile_url)
                df_profile["name"] = profile_name
                df_profile["last_updated"] = date_today
                list_users.append(df_profile)

                dict_pictures[profile_name] = {
                    "picture_data": self.download_profile_picture(),
                    "picfile": df_profile["picfile"].values[0]}

            except Exception as e:
                df_exceptions = df_exceptions.append({"name": profile_name, "error": str(e)}, ignore_index=True)
            log.info(f"Parsing {profile_name}: End")

        df_team = pd.concat(list_users)
        return df_team, dict_pictures, df_exceptions

    def parse_profile(self, url: str) -> pd.DataFrame:

        normalized_url = self.normalize_url(url)
        dict_profile = dict()
        dict_profile["linkedin"] = [normalized_url]

        self.driver.get(normalized_url)
        log.info(f"URL {normalized_url} loaded")
        Sleep.long()

        current_role = self.get_current_role()
        dict_profile["title"] = [current_role]
        log.info(f"Role {current_role} parsed")

        dict_profile["picfile"] = [self.get_picfile_name(normalized_url)]

        df_profile = pd.DataFrame(dict_profile)
        return df_profile

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
