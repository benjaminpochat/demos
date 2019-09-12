package org.demos.core.domains.webdocument;

import org.demos.core.domains.localgovernment.LocalGovernment;
import org.springframework.data.repository.CrudRepository;

import java.util.List;

public interface WebDocumentRepository extends CrudRepository<WebDocument, Long> {
    List<WebDocument> findByLocalGovernment(LocalGovernment localGovernment);
}
