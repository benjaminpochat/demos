package org.demos.core.domains.localgovernment;

import org.springframework.data.domain.Sort;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;

import java.util.List;
import java.util.Optional;

public interface LocalGovernmentRepository extends CrudRepository<LocalGovernment, Long> {
    List<LocalGovernment> findByWebSiteIsNotNull();

    @Query("select count(*) from LocalGovernment where webSite is not null")
    int countLocalGovernmentsWithWebSite();

    @Query( "select count(distinct localGov) " +
            "from LocalGovernment as localGov," +
            "       WebDocument as webDoc " +
            "where webDoc.localGovernment = localGov ")
    int countLocalGovernmentsWithWebDocuments();

    Optional<LocalGovernment> findByWebSite(String webSite);

    List<LocalGovernment> findFirst20ByNameStartingWithIgnoreCase(String name, Sort sort);

    @Query("select count(*) " +
            "from LocalGovernment as localGov " +
            "where webSite is not null " +
            "and webSite <> '' " +
            "and not exists (" +
            "select scrapingSession " +
            "from ScrapingSession as scrapingSession " +
            "where scrapingSession.localGovernment = localGov )")
    int countLocalGovernmentsWithWebSiteAndNoScrapingSession();

    @Query("select localGov " +
            "from LocalGovernment as localGov " +
            "where webSite is not null " +
            "and webSite <> '' " +
            "and not exists (" +
            "select scrapingSession " +
            "from ScrapingSession as scrapingSession " +
            "where scrapingSession.localGovernment = localGov )")
    List<LocalGovernment> findLocalGovernmentsWithWebSiteAndNoScrapingSession();

    @Query("select localGov " +
            "from LocalGovernment as localGov " +
            "inner join ScrapingSession scrapingSession on scrapingSession.localGovernment = localGov " +
            "order by scrapingSession.creation asc ")
    List<LocalGovernment> findLocalGovernmentWithWebSiteAndNotScrapedSinceLongestTime();
}
