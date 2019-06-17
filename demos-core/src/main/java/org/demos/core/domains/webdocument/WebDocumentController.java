package org.demos.core.domains.webdocument;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.Optional;

@RestController
public class WebDocumentController {

    @Autowired
    private WebDocumentRepository webDocumentRepository;

    @GetMapping(path = "/web-documents/{id}")
    public Optional<WebDocument> getWebDocument(@PathVariable Long id){
        return webDocumentRepository.findById(id);
    }

    @PostMapping(path = "/web-documents")
    public void createWebDocument(@Valid @RequestBody WebDocument webDocument){
        webDocumentRepository.save(webDocument);
    }

}
