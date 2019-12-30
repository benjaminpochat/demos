package org.demos.core.domains.scraping;

import org.demos.core.domains.localgovernment.LocalGovernment;
import org.demos.core.domains.localgovernment.LocalGovernmentRepository;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;
import java.util.concurrent.ThreadLocalRandom;

public class RotativeScrapingSessionFactory implements ScrapingSessionFactory {

    @Autowired
    LocalGovernmentRepository localGovernmentRepository;

    @Override
    public ScrapingSession createNewScrapingSession() {
        var scrapingSession = new ScrapingSession();
        if(localGovernmentRepository.countLocalGovernmentsWithWebSiteAndNoScrapingSession() > 0) {
            LocalGovernment localGovernment = getLocalGovernmentRandomly();
            scrapingSession.setLocalGovernment(localGovernment);
        } else {
            LocalGovernment localGovernment = getLocalGovernmentNotScrapedSinceLongestTime();
            scrapingSession.setLocalGovernment(localGovernment);
        }
        return scrapingSession;
    }

    private LocalGovernment getLocalGovernmentRandomly(){
        int nbLocalGovernments = localGovernmentRepository.countLocalGovernmentsWithWebSiteAndNoScrapingSession();
        List<LocalGovernment> allLocalGovernments = localGovernmentRepository.findLocalGovernmentsWithWebSiteAndNoScrapingSession();
        int randomLocalGovernmentIndex = ThreadLocalRandom.current().nextInt(0, nbLocalGovernments);
        return allLocalGovernments.get(randomLocalGovernmentIndex);
    }

    private LocalGovernment getLocalGovernmentNotScrapedSinceLongestTime() {
        return localGovernmentRepository.findLocalGovernmentWithWebSiteAndNotScrapedSinceLongestTime().get(0);
    }
}
