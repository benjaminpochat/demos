package org.demos.core.domains.scraping;

import org.assertj.core.api.Assertions;
import org.demos.commons.GenericBuilder;
import org.demos.core.domains.localgovernment.LocalGovernment;
import org.demos.core.domains.localgovernment.LocalGovernmentRepository;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;

@RunWith(SpringRunner.class)
@SpringBootTest
@Transactional
public class TestRotativeScrapingSessionFactory {

    @Autowired
    private LocalGovernmentRepository localGovernmentRepository;

    @Autowired
    private ScrapingSessionRepository scrapingSessionRepository;

    @Autowired
    private ScrapingSessionFactory scrapingSessionFactory;

    @Test
    public void createNewScrapingSession_should_use_a_local_government_with_no_scraping_session(){
        // given
        var paris = localGovernmentRepository.save(GenericBuilder.of(LocalGovernment::new)
                .with(LocalGovernment::setName, "Paris")
                .with(LocalGovernment::setWebSite, "www.paris.fr")
                .build());
        var annecy = localGovernmentRepository.save(GenericBuilder.of(LocalGovernment::new)
                .with(LocalGovernment::setName, "Annecy")
                .with(LocalGovernment::setWebSite, "www.annecy.fr")
                .build());
        var lyon = localGovernmentRepository.save(GenericBuilder.of(LocalGovernment::new)
                .with(LocalGovernment::setName, "Lyon")
                .build());
        var metz = localGovernmentRepository.save(GenericBuilder.of(LocalGovernment::new)
                .with(LocalGovernment::setName, "Metz")
                .with(LocalGovernment::setWebSite, "www.metz.fr")
                .build());
        var nantes = localGovernmentRepository.save(GenericBuilder.of(LocalGovernment::new)
                .with(LocalGovernment::setName, "Nantes")
                .with(LocalGovernment::setWebSite, "www.nantes.fr")
                .build());
        scrapingSessionRepository.save(GenericBuilder.of(ScrapingSession::new)
                .with(ScrapingSession::setCreation, LocalDateTime.now())
                .with(ScrapingSession::setLocalGovernment, nantes)
                .build());
        scrapingSessionRepository.save(GenericBuilder.of(ScrapingSession::new)
                .with(ScrapingSession::setCreation, LocalDateTime.now())
                .with(ScrapingSession::setLocalGovernment, paris)
                .build());

        // when
        ScrapingSession scrapingSession = scrapingSessionFactory.createNewScrapingSession();

        // then
        Assertions.assertThat(scrapingSession.getLocalGovernment().getName()).isIn("Annecy", "Metz");
    }

    @Test
    public void createNewScrapingSession_should_use_the_local_government_with_the_oldest_session(){
        // given
        var annecy = localGovernmentRepository.save(GenericBuilder.of(LocalGovernment::new)
                .with(LocalGovernment::setName, "Annecy")
                .with(LocalGovernment::setWebSite, "www.annecy.fr")
                .build());
        var metz = localGovernmentRepository.save(GenericBuilder.of(LocalGovernment::new)
                .with(LocalGovernment::setName, "Metz")
                .with(LocalGovernment::setWebSite, "www.metz.fr")
                .build());
        var lyon = localGovernmentRepository.save(GenericBuilder.of(LocalGovernment::new)
                .with(LocalGovernment::setName, "Lyon")
                .build());
        var nantes = localGovernmentRepository.save(GenericBuilder.of(LocalGovernment::new)
                .with(LocalGovernment::setName, "Nantes")
                .with(LocalGovernment::setWebSite, "www.nantes.fr")
                .build());
        scrapingSessionRepository.save(GenericBuilder.of(ScrapingSession::new)
                .with(ScrapingSession::setLocalGovernment, annecy)
                .build());
        scrapingSessionRepository.save(GenericBuilder.of(ScrapingSession::new)
                .with(ScrapingSession::setLocalGovernment, metz)
                .build());
        scrapingSessionRepository.save(GenericBuilder.of(ScrapingSession::new)
                .with(ScrapingSession::setLocalGovernment, nantes)
                .build());
        // when
        ScrapingSession scrapingSession = scrapingSessionFactory.createNewScrapingSession();

        // then
        Assertions.assertThat(scrapingSession.getLocalGovernment().getName()).isEqualTo("Annecy");
    }
}
