package org.demos.core;

import org.demos.core.domains.scraping.RandomScrapingSessionFactory;
import org.demos.core.domains.scraping.RotativeScrapingSessionFactory;
import org.demos.core.domains.scraping.ScrapingSessionFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

@SpringBootApplication
@EnableJpaAuditing
public class DemosCoreApplication {

	public static void main(String[] args) {
		SpringApplication.run(DemosCoreApplication.class, args);
	}

	@Bean
	public ScrapingSessionFactory getScrapingSessionFactory(){
		return new RotativeScrapingSessionFactory();
	}

}
