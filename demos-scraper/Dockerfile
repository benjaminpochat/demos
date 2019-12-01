FROM node:8.16.2-stretch-slim
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list
RUN wget https://dl-ssl.google.com/linux/linux_signing_key.pub
RUN apt-key add linux_signing_key.pub
RUN apt-get update
RUN apt-get --assume-yes install google-chrome-stable procps

RUN useradd --create-home demos
WORKDIR /home/demos
USER demos

COPY ./package.json ./package.json
COPY ./src ./src
RUN npm install --production

ENTRYPOINT ["node", "./src/main.js"]
