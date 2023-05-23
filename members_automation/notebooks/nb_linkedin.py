from notebooks.test_selenium import Keys
from notebooks.test_selenium import WebDriver

from src.utils import Sleep, _get_el

# TODO: need to change this so that these are not hardcoded.
LOGIN = "borja.elizaldejob@gmail.com"
PWD = "Pass8word8"


def perform_login(driver: WebDriver, pwd: str, login: str):
    driver.get("https://www.facebook.com/")
    Sleep.long()
    try:
        el_login = _get_el(
            driver=driver,
            id="email"
        )

        el_login.click()
        el_login.send_keys(login)
        Sleep.short()

        el_pwd = _get_el(
            driver=driver,
            id="pass",
        )

        el_pwd.click()
        el_pwd.send_keys(pwd)
        Sleep.short()

        el_pwd.send_keys(Keys.ENTER)
        Sleep.long()
    except:
        print("Already log in")
