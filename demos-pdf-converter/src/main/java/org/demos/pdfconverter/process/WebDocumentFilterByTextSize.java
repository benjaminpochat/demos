package org.demos.pdfconverter.process;


import org.demos.pdfconverter.model.WebDocument;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.function.Predicate;

public class WebDocumentFilterByTextSize implements Predicate<WebDocument> {

    private static final Logger LOGGER = LoggerFactory.getLogger(WebDocumentFilterByTextSize.class);

    /** The maximum content size in bytes
     * Default is set less than 1 MBytes which is the default maximum kafka message size
     */
    public static final int DEFAULT_MAXIMUM_TEXT_CONTENT_SIZE = 786432;

    private int maximumTextContentSize;

    public WebDocumentFilterByTextSize(int maximumTextContentSize) {
        this.maximumTextContentSize = maximumTextContentSize;
    }

    public WebDocumentFilterByTextSize() {
        this.maximumTextContentSize = DEFAULT_MAXIMUM_TEXT_CONTENT_SIZE;
    }

    @Override
    public boolean test(WebDocument webDocument) {
        UnclassifiedWebDocumentSerializer serializer = new UnclassifiedWebDocumentSerializer();
        byte[] serializedWebDocument = serializer.serialize(null, webDocument);
        if(serializedWebDocument.length < maximumTextContentSize){
            return true;
        }
        LOGGER.info("Document found at url " + webDocument.getUrl() + " is dropped from the processing stream and won't be sent to the classification process, because its text content larger than the limit fixed at " + maximumTextContentSize + " bytes.");
        return false;
    }
}
