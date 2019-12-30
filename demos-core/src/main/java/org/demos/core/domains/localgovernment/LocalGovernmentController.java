package org.demos.core.domains.localgovernment;

import org.demos.core.domains.webdocument.WebDocument;
import org.demos.core.domains.webdocument.WebDocumentController;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Sort;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Optional;

@RestController
public class LocalGovernmentController {

    @Autowired
    private LocalGovernmentRepository localGovernmentRepository;

    @Autowired
    private WebDocumentController webDocumentController;

    @GetMapping(path = "/localGovernments/{id}")
    public Optional<LocalGovernment> getLocalGovernment(@PathVariable Long id){
        return localGovernmentRepository.findById(id);
    }

    @GetMapping(path = "/localGovernments/searchByName/{name}")
    public List<LocalGovernment> searchLocalGovernmentByName(@PathVariable String name){
        return localGovernmentRepository.findFirst20ByNameStartingWithIgnoreCase(name, Sort.by("name"));
    }

    @GetMapping(path= "/localGovernments")
    public Optional<LocalGovernment> getLocalGovernmentByWebSite(@RequestParam(value = "webSite") String webSite){
        return localGovernmentRepository.findByWebSite(webSite);
    }

    @GetMapping(path= "/localGovernments/{id}/webDocuments")
    public List<WebDocument> getWebDocumentsByLocalGovernment(@PathVariable Long id){
        LocalGovernment localGovernment = new LocalGovernment();
        localGovernment.setId(id);
        return webDocumentController.getWebDocuments(localGovernment);
    }

}
