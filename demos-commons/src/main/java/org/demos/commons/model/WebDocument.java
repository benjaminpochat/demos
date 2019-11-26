package org.demos.core.domains.webdocument;

import org.demos.core.domains.localgovernment.LocalGovernment;

import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.ManyToOne;

@Entity
public class WebDocument {
    @Id
    private String id;

    private String url;

    @ManyToOne
    private LocalGovernment localGovernment;

    private String textContent;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public LocalGovernment getLocalGovernment() {
        return localGovernment;
    }

    public void setLocalGovernment(LocalGovernment localGovernment) {
        this.localGovernment = localGovernment;
    }

    public String getTextContent() {
        return textContent;
    }

    public void setTextContent(String textContent) {
        this.textContent = textContent;
    }
}
