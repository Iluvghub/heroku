FROM ghcr.io/iluvghub/heroku:latest

# Copies config(if it exists)
COPY . .

# Install requirements and start the bot
RUN npm install

#install requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# setup workdir


RUN dpkg --add-architecture i386 && apt-get update && apt-get -y dist-upgrade


