package org.demos.core.domains.localgovernment;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;

import java.util.Optional;

public interface LocalGovernmentRepository extends CrudRepository<LocalGovernment, Long> {
    Iterable<LocalGovernment> findByWebSiteIsNotNull();

    @Query("select count(*) from LocalGovernment where webSite is not null")
    Long countLocalGovernmentsWithWebSite();

    Optional<LocalGovernment> findByWebSite(String webSite);

}
