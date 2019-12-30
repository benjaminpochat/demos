package org.demos.core.domains.scraping;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;

import java.util.List;

public interface ScrapingSessionRepository extends CrudRepository<ScrapingSession, Long> {
    @Query("select localGov " +
            "from LocalGovernment as localGov " +
            "where webSite is not null and " +
            "not exists (" +
            "select scrapingSession " +
            "from ScrapingSession as scrapingSession " +
            "where scrapingSession.localGovernment = localGov )")
    List<ScrapingSession> findLocalGovernmentNotScrapedSinceLongestTime();
}
