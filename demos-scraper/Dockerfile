FROM node:8.16.2-stretch-slim
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list
RUN wget https://dl-ssl.google.com/linux/linux_signing_key.pub
RUN apt-key add linux_signing_key.pub
RUN apt-get update
RUN apt-get --assume-yes install google-chrome-stable procps
RUN apt-get install wait-for-it

RUN useradd --create-home demos
WORKDIR /home/demos
USER demos

COPY ./package.json ./package.json
COPY ./src ./src
RUN npm install --production

# Wait for java demos core application (localhost:80)
# and wait for kafka message bus (localhost:9092)
# and then start node scraping application
ENTRYPOINT ["wait-for-it", "localhost:8080", "--timeout=120", "--", "wait-for-it", "localhost:9092", "--timeout=120", "--", "node", "./src/main.js"]
