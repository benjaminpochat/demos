package org.demos.core.domains.scraping;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import javax.validation.Valid;

@RestController
public class ScrapingSessionController {

    @Autowired
    private ScrapingSessionRepository scrapingSessionRepository;

    @Autowired
    private ScrapingSessionFactory scrapingSessionFactory;

    @GetMapping(path = "/scrapingSessions")
    public ScrapingSession createScrapingSession(){
        ScrapingSession scrapingSession = scrapingSessionFactory.createNewScrapingSession();
        scrapingSession = scrapingSessionRepository.save(scrapingSession);
        return scrapingSession;
    }

    @PutMapping(path = "/scrapingSessions")
    public void updateScrapingSession(@Valid @RequestBody ScrapingSession scrapingSession){
        scrapingSessionRepository.save(scrapingSession);
    }
}
