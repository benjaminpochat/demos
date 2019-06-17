package org.demos.core.domains.localgovernment;

import javax.persistence.*;

@Entity
public class LocalGovernment {

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

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getWebSite() {
        return webSite;
    }

    public void setWebSite(String webSite) {
        this.webSite = webSite;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Float getLatitude() {
        return latitude;
    }

    public void setLatitude(Float latitude) {
        this.latitude = latitude;
    }

    public Float getLongitude() {
        return longitude;
    }

    public void setLongitude(Float longitude) {
        this.longitude = longitude;
    }

    public String getCodification() {
        return codification;
    }

    public void setCodification(String codification) {
        this.codification = codification;
    }

    public LocalGovernmentType getType() {
        return type;
    }

    public void setType(LocalGovernmentType type) {
        this.type = type;
    }
}
