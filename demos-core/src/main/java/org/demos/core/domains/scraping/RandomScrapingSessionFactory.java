package org.demos.core.domains.scraping;

import org.demos.core.domains.localgovernment.LocalGovernment;
import org.demos.core.domains.localgovernment.LocalGovernmentRepository;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;
import java.util.concurrent.ThreadLocalRandom;

public class RandomScrapingSessionFactory implements ScrapingSessionFactory {

    @Autowired
    private LocalGovernmentRepository localGovernmentRepository;

    @Override
    public ScrapingSession createNewScrapingSession() {
        ScrapingSession scrapingSession = new ScrapingSession();
        scrapingSession.setLocalGovernment(getLocalGovernmentRandomly());
        return scrapingSession;
    }

    public LocalGovernment getLocalGovernmentRandomly(){
        int nbLocalGovernments = localGovernmentRepository.countLocalGovernmentsWithWebSite();
        List<LocalGovernment> allLocalGovernments = localGovernmentRepository.findByWebSiteIsNotNull();
        int randomLocalGovernmentIndex = ThreadLocalRandom.current().nextInt(1, nbLocalGovernments);
        return allLocalGovernments.get(randomLocalGovernmentIndex);
    }
}
