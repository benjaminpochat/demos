# STEP 1 build static website
FROM node:10.9-alpine as builder
RUN apk update
WORKDIR /app
COPY ./demos-gui .
RUN cd /app && npm set progress=false && npm install
ARG configuration=production
RUN npm run build -- --configuration $configuration

# STEP 2 build a small nginx image with static website
FROM httpd:2.4.41-alpine
RUN rm /usr/local/apache2/htdocs/index.html
COPY --from=builder /app/dist/demos-gui /usr/local/apache2/htdocs/
