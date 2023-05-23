import urllib.request
from bs4 import BeautifulSoup
import base64
import requests

url = "https://proxy.scrapeops.io/v1/?api_key=912a36cb-f7af-4563-ada0-0d6147802579&url=https://www.linkedin.com/in/david-bofill-pages/"

website = urllib.request.urlopen(url)

mybytes = website.read()
html_doc = mybytes.decode("utf8")

website.close()

soup = BeautifulSoup(html_doc, features="lxml")
soup.prettify()
soup.title

soup.findAll("profile")

job_title = soup.find("h2").get_text(strip=True)

# Find the image tag with the specified link
image_tag = soup.find("meta", property="og:image")

# Extract the image link from the 'content' attribute
image_link = image_tag["content"]

image_data = base64.b64decode(image_content.split(',')[-1])

with open('image.jpg', 'wb') as file:
    file.write(image_data)

imgs = soup.findAll("img")
for img in imgs:
    print(img)

image_tag = soup.find("img")

src="https://media.licdn.com/dms/image/C4D03AQHX-FeAweRO-Q/profile-displayphoto-shrink_800_800/0/1658264136767?e=2147483647&amp;v=beta&amp;t=yrhp_1-R4YgNFE-M73-BRvTvcT3YmKXaVOOBNNUqT8M"

"https://proxy.scrapeops.io/v1/?api_key=912a36cb-f7af-4563-ada0-0d6147802579&url=https://media.licdn.com/dms/image/C4D03AQHX-FeAweRO-Q/profile-displayphoto-shrink_800_800/0/1658264136767?e=2147483647&amp;v=beta&amp;t=yrhp_1-R4YgNFE-M73-BRvTvcT3YmKXaVOOBNNUqT8M"

response = requests.get(image_link)

with open('image.jpg', 'wb') as file:
    file.write(response.content)
