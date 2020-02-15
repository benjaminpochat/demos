package org.demos.pdfconverter.process;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import org.demos.pdfconverter.model.WebDocument;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.concurrent.*;

public class PdfConverter {

    /**
     * Default timeout is set to 4 minutes, in order to be less than the default Kafka timeout "max.poll.interval.ms" set to 5 minutes .
     * (https://kafka.apache.org/documentation/)
     */
    public static final int DEFAULT_CONVERSION_TASK_TIMEOUT = 240000;

    private static Logger LOGGER = LoggerFactory.getLogger(PdfConverter.class);

    /**
     * Timeout for the conversion, in milliseconds
     */
    private int timeout;

    public int getTimeout() {
        return timeout;
    }

    public PdfConverter(int timeout) {
        this.timeout = timeout;
    }

    public PdfConverter(){
        this(DEFAULT_CONVERSION_TASK_TIMEOUT);
    }

    public WebDocument convert(WebDocument webDocument) {
        LOGGER.info("url " + webDocument.getUrl() + " is getting converted...");
        try {
            executeConversionTaskInWithinTimeoutDuration(webDocument);
        } catch (InterruptedException | ExecutionException | TimeoutException e) {
            LOGGER.error("An error occurs while converting " + webDocument.getUrl() + " into text.", e);
        }
        return webDocument;
    }

    void executeConversionTaskInWithinTimeoutDuration(WebDocument webDocument) throws InterruptedException, ExecutionException, TimeoutException {
        ExecutorService executor = Executors.newSingleThreadExecutor();
        Future future = executor.submit(getConversionTask(webDocument));
        future.get(getTimeout(), TimeUnit.MILLISECONDS);
    }

    ConversionTask getConversionTask(WebDocument webDocument) {
        return new ConversionTask(webDocument);
    }

    class ConversionTask implements Runnable {

        private WebDocument webDocument;

        ConversionTask(WebDocument webDocument) {
            this.webDocument = webDocument;
        }

        @Override
        public void run() {
            convertSilently();
        }

        private void convertSilently() {
            String parsedText = null;
            PDDocument pDDocument = null;
            try{
                pDDocument = PDDocument.load(webDocument.getPdfContent());
                PDFTextStripper pdfStripper = new PDFTextStripper();
                parsedText = pdfStripper.getText(pDDocument);
            } catch (Throwable t){
                LOGGER.error("An error occurs while converting " + webDocument.getUrl() + " into text.", t);
            } finally {
                closePDDocument(pDDocument);
            }
            webDocument.setTextContent(parsedText);
            webDocument.setPdfContent(null);
        }

        private void closePDDocument(PDDocument pDDocument) {
            if (pDDocument != null) {
                try {
                    pDDocument.close();
                } catch (IOException e) {
                    LOGGER.error("An critical error occurs while converting " + webDocument.getUrl() + " into text : PDDocument cannot be closed", e);
                }
            }
        }
    }
}
