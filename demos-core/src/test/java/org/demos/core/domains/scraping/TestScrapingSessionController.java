package org.demos.core.domains.scraping;

import org.assertj.core.api.Assertions;
import org.demos.commons.GenericBuilder;
import org.demos.core.domains.localgovernment.LocalGovernment;
import org.demos.core.domains.localgovernment.LocalGovernmentRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;

@SpringBootTest
@ExtendWith(SpringExtension.class)
@Transactional
public class TestScrapingSessionController {

    @Autowired
    ScrapingSessionController controller;

    @Autowired
    private LocalGovernmentRepository localGovernmentRepository;

    @Test
    public void createScrapingSession_should_return_a_session_with_a_new_id(){
        // given
        var paris = localGovernmentRepository.save(GenericBuilder.of(LocalGovernment::new)
                .with(LocalGovernment::setName, "Paris")
                .with(LocalGovernment::setWebSite, "www.paris.fr")
                .build());

        var beforeCreation = LocalDateTime.now();

        // when
        ScrapingSession scrapingSession = controller.createScrapingSession();

        // then
        var afterCreation = LocalDateTime.now();
        Assertions.assertThat(scrapingSession.getId()).isPositive();
        Assertions.assertThat(scrapingSession.getCreation()).isBetween(beforeCreation, afterCreation);
    }
}
