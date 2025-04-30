FROM python:3.12

WORKDIR /app

RUN pip install Flask flask-session Pillow
RUN apt-get update; apt-get install -y cabextract xfonts-utils fonts-liberation fonts-noto fonts-noto-cjk fonts-noto-color-emoji
RUN wget http://ftp.debian.org/debian/pool/contrib/m/msttcorefonts/ttf-mscorefonts-installer_3.8.1_all.deb \
    && apt install -y ./ttf-mscorefonts-installer_3.8.1_all.deb \
    && rm ttf-mscorefonts-installer_3.8.1_all.deb
RUN fc-cache -f

COPY . /app

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
