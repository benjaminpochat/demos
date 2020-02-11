package org.demos.pdfconverter.model;

import java.io.File;

public class WebDocument implements org.demos.model.domains.webdocument.WebDocument<LocalGovernment> {

    private String id;

    private String url;

    private LocalGovernment localGovernment;

    private String textContent;

    private byte[] pdfContent;

    @Override
    public String getId() {
        return id;
    }

    @Override
    public void setId(String id) {
        this.id = id;
    }

    @Override
    public String getUrl() {
        return url;
    }

    @Override
    public void setUrl(String url) {
        this.url = url;
    }

    @Override
    public LocalGovernment getLocalGovernment() {
        return localGovernment;
    }

    public void setLocalGovernment(LocalGovernment localGovernment) {
        this.localGovernment = localGovernment;
    }

    @Override
    public String getTextContent() {
        return textContent;
    }

    @Override
    public void setTextContent(String textContent) {
        this.textContent = textContent;
    }

    public byte[] getPdfContent() {
        return pdfContent;
    }

    public void setPdfContent(byte[] pdfContent) {
        this.pdfContent = pdfContent;
    }
}
