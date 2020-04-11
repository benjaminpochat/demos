package org.demos.core.domains.scrapingstatistics;

import org.demos.core.domains.localgovernment.LocalGovernmentRepository;
import org.demos.core.domains.webdocument.WebDocumentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ScrapingStatisticsController {

    @Autowired
    private LocalGovernmentRepository localGovernmentRepository;

    @Autowired
    private WebDocumentRepository webDocumentRepository;

    @GetMapping(path = "/scrapingStatistics")
    ScrapingStatistics computeScrapingStatistics(){
        ScrapingStatistics statistics = new ScrapingStatistics();
        statistics.setLocalGovernmentWithWebDocumentsCollected(localGovernmentRepository.countLocalGovernmentsWithWebDocuments());
        statistics.setWebDocumentsCollected(webDocumentRepository.count());
        return statistics;
    }
}
