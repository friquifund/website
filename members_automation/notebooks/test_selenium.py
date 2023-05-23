from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("headless")

exe_path = ChromeDriverManager().install()
service = Service(exe_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.linkedin.com/login")
sleep(6)

linkedin_username = "borja.elizaldejob@gmail.com"
linkedin_password = "Pass8word8"

driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/form/div[\
                              1]/input").send_keys(linkedin_username)
driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/form/div[\
                              2]/input").send_keys(linkedin_password)
sleep(3)
driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/form/div[\
                              3]/button").click()

profiles = ['https://www.linkedin.com/in/vinayak-rai-a9b231193/',
            'https://www.linkedin.com/in/dishajindgar/',
            'https://www.linkedin.com/in/ishita-rai-28jgj/']

for i in profiles:
    driver.get(i)
    sleep(5)
    title = driver.find_element(By.XPATH,
                                "//h1[@class='text-heading-xlarge inline t-24 v-align-middle break-words']").text
    print(title)
    description = driver.find_element(By.XPATH,
                                      "//div[@class='text-body-medium break-words']").text
    print(description)
    sleep(4)
driver.close()