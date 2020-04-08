package org.demos.model.domains.localgovernment;

import java.util.Map;

public interface LocalGovernment {

    public Long getId();

    public void setId(Long id);

    public String getWebSite();

    public void setWebSite(String webSite);

    public String getName();

    public void setName(String name);

    public Float getLatitude();

    public void setLatitude(Float latitude);

    public Float getLongitude();

    public void setLongitude(Float longitude);

    public String getCodification();

    public void setCodification(String codification);

    public LocalGovernmentType getType();

    public void setType(LocalGovernmentType type);

    public String getZipCode();

    public void setZipCode(String zipCode);
}
