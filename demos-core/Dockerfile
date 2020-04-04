# Must be used with demos root folder as docker context.
# For instance : docker build ~/demos -f ~/demos/demos-core/Dockerfile

FROM maven:3.6.1-jdk-11-slim

RUN apt-get update
RUN apt-get install wait-for-it

RUN chmod -R a+rwx /usr/share/maven
RUN useradd --create-home demos
WORKDIR /home/demos

COPY ./pom.xml ./pom.xml
COPY ./demos-model ./demos-model
COPY ./demos-core ./demos-core

RUN mvn clean install -N -s /usr/share/maven/ref/settings-docker.xml -f ./pom.xml
RUN mvn clean install -s /usr/share/maven/ref/settings-docker.xml -f ./demos-model/pom.xml
RUN mvn clean install -s /usr/share/maven/ref/settings-docker.xml -f ./demos-core/pom.xml
RUN mvn exec:java -s /usr/share/maven/ref/settings-docker.xml -f ./demos-core/pom.xml -Dexec.skip=true

USER demos

ENV demos.datasource.url=${demos.datasource.url}
ENV demos.datasource.user=${demos.datasource.user}
ENV demos.datasource.password=${demos.datasource.password}

# Wait for Postgre database (localhost:5432)
# and then start java core application
ENTRYPOINT ["wait-for-it", "localhost:5432", "--timeout=120", "--", "mvn", "exec:java", "-s", "/usr/share/maven/ref/settings-docker.xml", "-f", "./demos-core/pom.xml", "-Dspring.profiles.active=prod", "-Dspring.datasource.url=${demos.datasource.url}", "-Dspring.datasource.user=${demos.datasource.user}", "-Dspring.datasource.password=${demos.datasource.password}"]
