package org.demos.pdfconverter.model;

import org.demos.model.domains.localgovernment.LocalGovernmentType;

public class LocalGovernment implements org.demos.model.domains.localgovernment.LocalGovernment {
    private Long id;

    private String webSite;

    private String name;

    private LocalGovernmentType type;

    private Float latitude;

    private Float longitude;

    private String codification;

    private String zipCode;

    @Override
    public Long getId() {
        return id;
    }

    @Override
    public void setId(Long id) {
        this.id = id;
    }

    @Override
    public String getWebSite() {
        return webSite;
    }

    @Override
    public void setWebSite(String webSite) {
        this.webSite = webSite;
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public void setName(String name) {
        this.name = name;
    }

    @Override
    public LocalGovernmentType getType() {
        return type;
    }

    @Override
    public void setType(LocalGovernmentType type) {
        this.type = type;
    }

    @Override
    public Float getLatitude() {
        return latitude;
    }

    @Override
    public void setLatitude(Float latitude) {
        this.latitude = latitude;
    }

    @Override
    public Float getLongitude() {
        return longitude;
    }

    @Override
    public void setLongitude(Float longitude) {
        this.longitude = longitude;
    }

    @Override
    public String getCodification() {
        return codification;
    }

    @Override
    public void setCodification(String codification) {
        this.codification = codification;
    }

    @Override
    public String getZipCode() {
        return zipCode;
    }

    @Override
    public void setZipCode(String zipCode) {
        this.zipCode = zipCode;
    }
}
