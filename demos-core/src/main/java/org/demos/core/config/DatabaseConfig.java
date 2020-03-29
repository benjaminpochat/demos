package org.demos.core.config;

import org.springframework.boot.jdbc.DataSourceBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;

import javax.sql.DataSource;

@Configuration
@Profile("prod")
public class DatabaseConfig {

    @Bean
    public DataSource dataSource() {
        return DataSourceBuilder
                .create()
                .username("demos")
                .password("d3m0z")
                .url("jdbc:postgresql://localhost:5432/demos")
            .build();
    }
}
