FROM python:3.9

ENV GECKODRIVER_VER v0.30.0
ENV FIREFOX_VER 87.0

RUN set -x \
   && apt update \
   && apt upgrade -y \
   && apt install -y \
       firefox-esr

# Add latest FireFox
RUN set -x \
   && apt install -y \
       libx11-xcb1 \
       libdbus-glib-1-2 \
   && curl -sSLO https://download-installer.cdn.mozilla.net/pub/firefox/releases/${FIREFOX_VER}/linux-x86_64/en-US/firefox-${FIREFOX_VER}.tar.bz2 \
   && tar -jxf firefox-* \
   && mv firefox /opt/ \
   && chmod 755 /opt/firefox \
   && chmod 755 /opt/firefox/firefox      

# Add geckodriver
RUN set -x \
   && curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
   && tar zxf geckodriver-*.tar.gz \
   && mv geckodriver /usr/bin/

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./src /app

RUN mkdir downloads
RUN mkdir -p config/retry

WORKDIR /app

# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout app.log \
	&& ln -sf /dev/stderr app.log

ENTRYPOINT ["python", "./main.py"]