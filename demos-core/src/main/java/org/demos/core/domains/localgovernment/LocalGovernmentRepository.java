package org.demos.core.domains.localgovernment;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;

public interface LocalGovernmentRepository extends CrudRepository<LocalGovernment, Long> {
    Iterable<LocalGovernment> findByWebSiteIsNotNull();

    @Query("select count(*) from LocalGovernment where webSite is not null")
    Long countLocalGovernmentsWithWebSite();
}
