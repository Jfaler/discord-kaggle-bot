# Download base image Ubuntu 18.04
FROM ubuntu:18.04

# Update software & install Kaggle Discord bot
RUN apt-get update
RUN apt-get install python3.7
RUN apt-get install pip3
RUN pip3 install -r requirements.txt
CMD cd discord-kaggle-bot && python3 main.py
