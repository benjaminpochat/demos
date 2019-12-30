package org.demos.model.domains.scraping;

import org.demos.model.domains.localgovernment.LocalGovernment;

import java.time.LocalDateTime;

public interface ScrapingSession<T extends LocalGovernment> {
    public Long getId();
    public void setId();
    public LocalDateTime getCreation();
    public void setCreation(LocalDateTime creation);
    public LocalDateTime getEndScraping();
    public void setEndScraping(LocalDateTime endScraping);
    public T getLocalGovernment();
    public void setLocalGovernment(T localGovernment);
}
