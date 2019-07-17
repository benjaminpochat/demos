FROM maven:3.6.1-jdk-11-slim

RUN useradd --create-home demos
WORKDIR /home/demos
USER demos

COPY ./demos-core/src ./src
COPY ./demos-core/pom.xml ./pom.xml

RUN mvn clean install -DskipTests
RUN mvn exec:java -Dexec.skip=true

ENTRYPOINT ["mvn", "exec:java", "-Ddemos.datasource.url=${demos.datasource.url}", "-Ddemos.datasource.user=${demos.datasource.user}", "-Ddemos.datasource.password=${demos.datasource.password}"]
