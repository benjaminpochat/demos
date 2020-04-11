package org.demos.core.domains.webdocument;

import org.demos.core.domains.localgovernment.LocalGovernment;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.Collection;
import java.util.List;
import java.util.Optional;

@RestController
public class WebDocumentController {

    @Autowired
    private WebDocumentRepository webDocumentRepository;

    @GetMapping(path = "/webDocuments/{id}")
    public Optional<WebDocument> getWebDocument(@PathVariable String id){
        return webDocumentRepository.findById(id);
    }

    @GetMapping(path = "/webDocuments")
    public Iterable<WebDocument> getWebDocuments(){
        return webDocumentRepository.findAll();
    }
    
    @PostMapping(path = "/webDocuments")
    public void createWebDocument(@Valid @RequestBody WebDocument webDocument){
        webDocumentRepository.save(webDocument);
    }

    public List<WebDocument> getWebDocuments(LocalGovernment localGovernment) {
        return webDocumentRepository.findByLocalGovernment(localGovernment);
    }
}
