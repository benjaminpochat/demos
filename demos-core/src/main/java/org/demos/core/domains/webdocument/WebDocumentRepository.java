package org.demos.core.domains.webdocument;

import org.demos.core.domains.localgovernment.LocalGovernment;
import org.springframework.data.repository.CrudRepository;

import java.util.List;
import java.util.Optional;

public interface WebDocumentRepository extends CrudRepository<WebDocument, Long> {
    Optional<WebDocument> findById(String id);

    List<WebDocument> findByLocalGovernment(LocalGovernment localGovernment);
}
