# Need to install chrome and to install chromestable
#3https://stackoverflow.com/questions/73152015/seleniun-python-not-running-in-docker
FROM --platform=linux/amd64 python:3.8

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

RUN mkdir /logs
ENV LOG=/logs
# Copy the rest of the code
COPY . app/
WORKDIR /app

RUN pip install -e .

#CMD ["python", "entrypoint_python.py"]
