package org.demos.pdfconverter.process;


import org.demos.pdfconverter.model.WebDocument;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.function.Predicate;

public class WebDocumentFilterByPdfContent implements Predicate<WebDocument> {

    private static final Logger LOGGER = LoggerFactory.getLogger(WebDocumentFilterByPdfContent.class);

    @Override
    public boolean test(WebDocument webDocument) {
        if(webDocument.getPdfContent() != null && webDocument.getPdfContent().length > 0){
            return true;
        }
        LOGGER.info("Document found at url " + webDocument.getUrl() + " is dropped from the processing stream and won't be sent to the classification process, because no pdf content has been downloaded.");
        return false;
    }
}
