FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y xvfb
RUN apt-get install -qqy x11-apps

# chromium dependencies
RUN apt-get install -y libnss3 \
  libxss1 \
  libasound2 \
  fonts-noto-color-emoji

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN playwright install-deps

RUN playwright install

COPY . .

ENTRYPOINT ["/bin/sh", "-c", "/usr/bin/xvfb-run -a $@", ""] 

