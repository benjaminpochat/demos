package org.demos.core.domains.localgovernment;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.util.Optional;

@RestController
public class LocalGovernmentController {

    @Autowired
    private LocalGovernmentRepository localGovernmentRepository;

    @GetMapping(path = "/local-governments/{id}")
    public Optional<LocalGovernment> getLocalGovernment(@PathVariable Long id){
        return localGovernmentRepository.findById(id);
    }

    @GetMapping(path = "/local-governments?for-scraping=true&result-size=1")
    public LocalGovernment getLocalGovernmentForScraping(){
        //return localGovernmentRepository.findRandomly;
        return null;
    }

}
