FROM python:3.8

WORKDIR /home

ENV TELEGRAM_API_TOKEN=""
ENV TELEGRAM_ACCESS_ID=""
ENV TELEGRAM_PROXY_URL=""
ENV TELEGRAM_PROXY_LOGIN=""
ENV TELEGRAM_PROXY_PASSWORD=""

RUN pip install python-telegram-bot --upgrade
RUN pip install requests
RUN pip install xlrd

EXPOSE 443 80 22

COPY *.py ./

RUN python main.py
