package org.demos.core.domains.localgovernment;

import org.springframework.data.domain.Sort;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;

import java.util.List;
import java.util.Optional;

public interface LocalGovernmentRepository extends CrudRepository<LocalGovernment, Long> {
    Iterable<LocalGovernment> findByWebSiteIsNotNull();

    @Query("select count(*) from LocalGovernment where webSite is not null")
    Long countLocalGovernmentsWithWebSite();

    @Query( "select count(distinct localGov) " +
            "from LocalGovernment as localGov," +
            "       WebDocument as webDoc " +
            "where webDoc.localGovernment = localGov ")
    Long countLocalGovernmentsWithWebDocuments();

    Optional<LocalGovernment> findByWebSite(String webSite);

    List<LocalGovernment> findFirst20ByNameStartingWithIgnoreCase(String name, Sort sort);

}
