import os
import random
import time
from typing import Any, Dict, List, Optional, Tuple

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class Sleep:
    @staticmethod
    def short():
        time.sleep(random.uniform(0.5, 1.2))

    @staticmethod
    def med():
        time.sleep(random.uniform(1.2, 2.5))

    @staticmethod
    def long():
        time.sleep(random.uniform(2.5, 3.1))

    @staticmethod
    def extra_long():
        time.sleep(random.uniform(10.5, 20.1))


def get_driver_plain() -> webdriver:

    options = webdriver.ChromeOptions()
    prefs = {
        "profile.default_content_setting_values": {
            "cookies": 2,
            "images": 2,
            # "javascript": 2,
            "plugins": 2,
            "popups": 2,
            "geolocation": 2,
            "notifications": 2,
            "auto_select_certificate": 2,
            "fullscreen": 2,
            "mouselock": 2,
            "mixed_script": 2,
            "media_stream": 2,
            "media_stream_mic": 2,
            "media_stream_camera": 2,
            "protocol_handlers": 2,
            "ppapi_broker": 2,
            "automatic_downloads": 2,
            "midi_sysex": 2,
            "push_messaging": 2,
            "ssl_cert_decisions": 2,
            "metro_switch_to_desktop": 2,
            "protected_media_identifier": 2,
            "app_banner": 2,
            "site_engagement": 2,
            "durable_storage": 2,
        },
        "profile.managed_default_content_settings.javascript": 2,
    }
    options.add_experimental_option("prefs", prefs)

    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(
        executable_path="../../post_ads/chromedriver.exe", chrome_options=options
    )

    return driver


def kill_driver():
    os.system("taskkill /im chromedriver.exe /T /f")
    os.system("taskkill /im jcef_helper.exe /T /f")


def get_driver() -> webdriver:
    kill_driver()

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-data-dir=/Users/elizaldeborja/Library/Application Support/")
    options.add_argument("--profile-directory=Default")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option(
        "prefs", {"profile.default_content_setting_values.notifications": 2}
    )
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--incognito")
    #options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    #options.add_argument("--no-sandbox")
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})

    chromedriver_path = "/opt/homebrew/bin/chromedriver"
    #chromedriver_path = "/usr/bin/chromedriver"
    #driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    #executable_path = chromedriver_path
    driver = webdriver.Chrome(chrome_options=options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    driver.delete_all_cookies()

    Sleep.med()
    return driver


def _get_el(
    driver: webdriver,
    *,
    id: Optional[str] = None,
    tag_name: Optional[str] = None,
    text: Optional[str] = None,
    prop_name_val_pair: Optional[Tuple[str, str]] = None,
    attr_name_val_pair: Optional[Tuple[str, str]] = None,
    use_first: Optional[bool] = False,
    in_element: Optional[WebElement] = None,
):

    finder = driver if in_element is None else in_element

    if id is not None:
        return finder.find_element(By.ID, id)

    msg = "Need 'tag_name' if 'id' not supplied"
    assert tag_name is not None, msg

    els = finder.find_elements(By.TAG_NAME, tag_name)

    if text is not None:
        els_reqd = [x for x in els if x.text == text]
        msg = f"""
        error searching els with tag name: '{tag_name}' 
        with text: '{text}' 
        """
    elif prop_name_val_pair is not None:
        prop_name = prop_name_val_pair[0]
        prop_val = prop_name_val_pair[1]

        els_reqd = [x for x in els if x.get_property(prop_name) == prop_val]

        msg = f"""
        error searching els with tag name: '{tag_name}' 
        with prop: '{prop_name}' 
        of val '{prop_val}' 
        """
    elif attr_name_val_pair is not None:
        attr_name = attr_name_val_pair[0]
        attr_val = attr_name_val_pair[1]

        els_reqd = [x for x in els if x.get_attribute(attr_name) == attr_val]

        msg = f"""
        error searching els with tag name: '{tag_name}' 
        with prop: '{attr_name}' 
        of val '{attr_val}' 
        """
    else:
        raise Exception("not enough params supplied")

    assert len(els_reqd) > 0, msg + "NONE FOUND"

    if not use_first:
        assert len(els_reqd) == 1, msg + "MORE THAN ONE FOUND"

    el = els_reqd[0]

    return el

