FROM maven:3.6.1-jdk-11-slim

WORKDIR /usr/src/app
COPY ./demos-core/src /usr/src/app/src
COPY ./demos-core/pom.xml /usr/src/app/pom.xml
RUN mvn clean install -DskipTests
RUN mvn exec:java -Dexec.skip=true
ENTRYPOINT ["mvn", "exec:java", "-Ddemos.datasource.url=${demos.datasource.url}", "-Ddemos.datasource.user=${demos.datasource.user}", "-Ddemos.datasource.password=${demos.datasource.password}"]
