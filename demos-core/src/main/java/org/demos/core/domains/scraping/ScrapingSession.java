package org.demos.core.domains.scraping;

import org.demos.core.domains.localgovernment.LocalGovernment;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import javax.persistence.*;
import java.time.LocalDateTime;

@Entity
@EntityListeners(AuditingEntityListener.class)
public class ScrapingSession implements org.demos.model.domains.scraping.ScrapingSession<LocalGovernment> {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "scraping_session_id_generator")
    @SequenceGenerator(name="scraping_session_id_generator", sequenceName = "scraping_session_id_seq", allocationSize = 1)
    @Column(name = "id", updatable = false, nullable = false)
    private Long id;

    @CreatedDate
    private LocalDateTime creation;

    private LocalDateTime endScraping;

    @ManyToOne
    private LocalGovernment localGovernment;

    @Override
    public Long getId() {
        return id;
    }

    @Override
    public void setId() {
        this.id = id;
    }

    @Override
    public LocalDateTime getCreation() {
        return creation;
    }

    @Override
    public void setCreation(LocalDateTime creation) {
        this.creation = creation;
    }

    @Override
    public LocalDateTime getEndScraping() {
        return endScraping;
    }

    @Override
    public void setEndScraping(LocalDateTime endScraping) {
        this.endScraping = endScraping;
    }

    @Override
    public LocalGovernment getLocalGovernment() {
        return localGovernment;
    }

    @Override
    public void setLocalGovernment(LocalGovernment localGovernment) {
        this.localGovernment = localGovernment;
    }
}
