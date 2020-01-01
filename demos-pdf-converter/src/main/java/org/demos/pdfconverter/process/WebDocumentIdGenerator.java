package org.demos.pdfconverter.process;

import org.apache.commons.codec.digest.DigestUtils;
import org.demos.pdfconverter.model.WebDocument;

public class WebDocumentIdGenerator {

    public WebDocument generateId(WebDocument webDocument) {
        webDocument.setId(DigestUtils.sha256Hex(webDocument.getTextContent()));
        return webDocument;
    }

}
