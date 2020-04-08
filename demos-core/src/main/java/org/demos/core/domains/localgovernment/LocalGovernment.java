package org.demos.core.domains.localgovernment;

import org.demos.model.domains.localgovernment.LocalGovernmentType;

import javax.persistence.*;
import java.util.Map;
import java.util.Set;

@Entity
public class LocalGovernment implements org.demos.model.domains.localgovernment.LocalGovernment<LocalGovernment> {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "local_government_id_generator")
    @SequenceGenerator(name="local_government_id_generator", sequenceName = "local_government_id_seq", allocationSize = 1)
    @Column(name = "id", updatable = false, nullable = false)
    private Long id;

    private String webSite;

    private String name;

    @Enumerated(EnumType.STRING)
    private LocalGovernmentType type;

    private Float latitude;

    private Float longitude;

    private String codification;

    private String zipCode;

    @ManyToMany
    @MapKeyEnumerated(EnumType.STRING)
    private Map<LocalGovernmentType, LocalGovernment> overlappingLocalGovernments;

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
    public LocalGovernmentType getType() {
        return type;
    }

    @Override
    public void setType(LocalGovernmentType type) {
        this.type = type;
    }

    @Override
    public String getZipCode() {
        return zipCode;
    }

    @Override
    public void setZipCode(String zipCode) {
        this.zipCode = zipCode;
    }

    @Override
    public Map<LocalGovernmentType, LocalGovernment> getOverlappingLocalGovernments() {
        return overlappingLocalGovernments;
    }

    @Override
    public void setOverlappingLocalGovernments(Map<LocalGovernmentType, LocalGovernment> overlappingLocalGovernments) {
        this.overlappingLocalGovernments = overlappingLocalGovernments;
    }

    @Override
    public LocalGovernment getOverlappingLocalGovernment(LocalGovernmentType type){
        return overlappingLocalGovernments.get(type);
    }
}
