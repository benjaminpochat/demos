package org.demos.core.domains.localgovernment;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.util.Iterator;
import java.util.Optional;
import java.util.concurrent.ThreadLocalRandom;

@RestController
public class LocalGovernmentController {

    @Autowired
    private LocalGovernmentRepository localGovernmentRepository;

    @GetMapping(path = "/localGovernments/forScraping")
    public LocalGovernment getLocalGovernmentForScraping(){
        long nbLocalGovernments = localGovernmentRepository.countLocalGovernmentsWithWebSite();
        Iterator<LocalGovernment> allLocalGovernmentsIterator = localGovernmentRepository.findByWebSiteIsNotNull().iterator();
        long randomLocalGovernemntIndex = ThreadLocalRandom.current().nextLong(1, nbLocalGovernments);
        for (long i = 0 ; i < randomLocalGovernemntIndex ; i++) {
            allLocalGovernmentsIterator.next();
        }
        return allLocalGovernmentsIterator.next();
    }

    @GetMapping(path = "/localGovernments/{id}")
    public Optional<LocalGovernment> getLocalGovernment(@PathVariable Long id){
        return localGovernmentRepository.findById(id);
    }

}
