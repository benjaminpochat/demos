package org.demos.model.domains.webdocument;

import org.demos.model.domains.localgovernment.LocalGovernment;

public interface WebDocument<G extends LocalGovernment> {
    public String getId();

    public void setId(String id);

    public String getUrl();

    public void setUrl(String url);

    public G getLocalGovernment();

    public void setLocalGovernment(G localGovernment);

    public String getTextContent();

    public void setTextContent(String textContent);
}
