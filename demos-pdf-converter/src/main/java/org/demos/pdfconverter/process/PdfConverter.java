package org.demos.pdfconverter.process;

import org.apache.pdfbox.io.MemoryUsageSetting;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import org.demos.pdfconverter.model.WebDocument;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.net.URLConnection;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
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

    /**
     * The maximum size of temporary PDF files (see {@link MemoryUsageSetting#setupMainMemoryOnly(long)}
     */
    private long maximumTemporaryFilesSize;

    public int getTimeout() {
        return timeout;
    }

    public PdfConverter(int timeout, long maximumTemporaryFilesSize) {
        this.timeout = timeout;
        this.maximumTemporaryFilesSize = maximumTemporaryFilesSize;
    }

    public PdfConverter(){
        this(DEFAULT_CONVERSION_TASK_TIMEOUT, -1);
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

    PDDocument getPDDocument(InputStream inputStream) throws IOException {
        return PDDocument.load(inputStream, MemoryUsageSetting.setupTempFileOnly(maximumTemporaryFilesSize));
    }

    private void initSSLSocketFactory() throws NoSuchAlgorithmException, KeyManagementException {
        TrustManager[] trustAllCerts = getTrustManagers();
        SSLContext sslContext = SSLContext.getInstance("SSL");
        sslContext.init(null, trustAllCerts, new java.security.SecureRandom());
        HttpsURLConnection.setDefaultSSLSocketFactory(sslContext.getSocketFactory());
    }

    private TrustManager[] getTrustManagers() {
        return new TrustManager[]{
            new X509TrustManager() {
                public java.security.cert.X509Certificate[] getAcceptedIssuers() {
                    return null;
                }
                public void checkClientTrusted(
                        java.security.cert.X509Certificate[] certs, String authType) {
                }
                public void checkServerTrusted(
                        java.security.cert.X509Certificate[] certs, String authType) {
                }
            }
        };
    }

    class ConversionTask implements Runnable {

        private WebDocument webDocument;

        ConversionTask(WebDocument webDocument) {
            this.webDocument = webDocument;
        }

        @Override
        public void run() {
            String parsedText = null;
            PDDocument pDDocument = null;
            try{
                initSSLSocketFactory();
                URL url = new URL(webDocument.getUrl());
                URLConnection urlConnection = url.openConnection();
                InputStream inputStream = urlConnection.getInputStream();
                pDDocument = getPDDocument(inputStream);
                PDFTextStripper pdfStripper = new PDFTextStripper();
                parsedText = pdfStripper.getText(pDDocument);
            } catch (Throwable t){
                LOGGER.error("An error occurs while converting " + webDocument.getUrl() + " into text.", t);
            } finally {
                closePDDocument(pDDocument);
            }
            webDocument.setTextContent(parsedText);
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
