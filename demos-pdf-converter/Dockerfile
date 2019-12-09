# Must be used with demos root folder as docker context.
# For instance : docker build ~/demos -f ~/demos/demos-pdf-converter/Dockerfile

FROM maven:3.6.1-jdk-11-slim

RUN apt-get update
RUN apt-get install wait-for-it

RUN chmod -R a+rwx /usr/share/maven
RUN useradd --create-home demos
WORKDIR /home/demos

COPY ./pom.xml ./pom.xml
COPY ./demos-model ./demos-model
COPY ./demos-pdf-converter ./demos-pdf-converter

RUN mvn clean install -N -s /usr/share/maven/ref/settings-docker.xml -f ./pom.xml
RUN mvn clean install -DskipTests -s /usr/share/maven/ref/settings-docker.xml -f ./demos-model/pom.xml
RUN mvn clean install -DskipTests -s /usr/share/maven/ref/settings-docker.xml -f ./demos-pdf-converter/pom.xml
RUN mvn exec:java -Dexec.skip=true -s /usr/share/maven/ref/settings-docker.xml -f ./demos-pdf-converter/pom.xml

USER demos

# Wait for kafka message bus (localhost:9092)
# and then start java pdf converter
ENTRYPOINT ["wait-for-it", "localhost:9092", "--", "mvn", "exec:java", "-s", "/usr/share/maven/ref/settings-docker.xml", "-f", "./demos-pdf-converter/pom.xml"]
