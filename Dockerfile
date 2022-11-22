FROM python:3.9.15-slim-bullseye
# WORKDIR /home
EXPOSE 8080
# COPY ./setup.sh /
# COPY ./requirements.txt /
RUN apt-get update && apt -y install git \
    ca-certificates fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 libgcc1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 lsb-release wget xdg-utils \
    && rm -rf /var/lib/apt/lists/*
    # && pip install -r /requirements.txt \
    # && pyppeteer-install

RUN useradd -m -d /bot -s /bin/bash bot
USER bot
WORKDIR /bot
# this is the directory in which pip3 will install binaries
ENV PATH=/bot/.local/bin:$PATH
# ADD . /bot
COPY ./setup.sh /bot
COPY ./requirements.txt /bot

RUN pip install --user -r requirements.txt \
    && pyppeteer-install
ENTRYPOINT ["/bot/setup.sh"]