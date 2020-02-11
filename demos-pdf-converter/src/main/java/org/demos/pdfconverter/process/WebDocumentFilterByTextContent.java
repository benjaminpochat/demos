package org.demos.pdfconverter.process;

import org.demos.pdfconverter.model.WebDocument;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.function.Predicate;

public class WebDocumentFilterByTextContent implements Predicate<WebDocument> {

    private final static Logger LOGGER = LoggerFactory.getLogger(WebDocumentFilterByTextContent.class);

    @Override
    public boolean test(WebDocument webDocument) {
        if(webDocument.getTextContent() != null){
            return true;
        }
        LOGGER.info("Document found at url " + webDocument.getUrl() + " is dropped from the processing stream and won't be sent to the classification process, because its text content is null.");
        return false;
    }
}
