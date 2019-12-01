FROM maven:3.6.1-jdk-11-slim

RUN chmod -R a+rwx /usr/share/maven
RUN useradd --create-home demos
WORKDIR /home/demos

COPY ./pom.xml ./pom.xml
COPY ./demos-model ./demos-model
COPY ./demos-pdf-converter ./demos-pdf-converter

RUN mvn clean install -N -s /usr/share/maven/ref/settings-docker.xml -f ./pom.xml
RUN mvn clean install -DskipTests -s /usr/share/maven/ref/settings-docker.xml -f ./demos-model/pom.xml
RUN mvn clean compile -DskipTests -s /usr/share/maven/ref/settings-docker.xml -f ./demos-pdf-converter/pom.xml
RUN mvn exec:java -Dexec.skip=true -s /usr/share/maven/ref/settings-docker.xml -f ./demos-pdf-converter/pom.xml

USER demos

ENTRYPOINT ["mvn", "exec:java", "-s", "/usr/share/maven/ref/settings-docker.xml", "-f", "./demos-pdf-converter/pom.xml"]
