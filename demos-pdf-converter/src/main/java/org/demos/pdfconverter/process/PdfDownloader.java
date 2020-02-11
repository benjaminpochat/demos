package org.demos.pdfconverter.process;

import org.demos.pdfconverter.model.WebDocument;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.net.URLConnection;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.util.concurrent.*;

public class PdfDownloader {

    public static final int DEFAULT_DOWNLOAD_TASK_TIMEOUT = 240000;

    private static Logger LOGGER = LoggerFactory.getLogger(PdfDownloader.class);

    private int maximumPdfContentSizeInBytes;

    /**
     * Timeout for download, in milliseconds
     */
    private int timeout;

    public int getTimeout() {
        return timeout;
    }

    public PdfDownloader(int maximumPdfContentSizeInBytes, int timeout) {
        this.maximumPdfContentSizeInBytes = maximumPdfContentSizeInBytes;
        this.timeout = timeout;
    }

    public PdfDownloader(int maximumPdfContentSizeInBytes) {
        this(maximumPdfContentSizeInBytes, DEFAULT_DOWNLOAD_TASK_TIMEOUT);
    }

    public WebDocument download(WebDocument webDocument){
        LOGGER.info("url " + webDocument.getUrl() + " is getting downloaded...");
        try {
            executeDownloadTaskInWithinTimeoutDuration(webDocument);
        } catch (InterruptedException | ExecutionException | TimeoutException e) {
            LOGGER.error("An error occurs while downloading " + webDocument.getUrl() + ".", e);
        }
        return webDocument;
    }

    void executeDownloadTaskInWithinTimeoutDuration(WebDocument webDocument) throws InterruptedException, ExecutionException, TimeoutException {
        ExecutorService executor = Executors.newSingleThreadExecutor();
        Future future = executor.submit(getDownloadTask(webDocument));
        future.get(getTimeout(), TimeUnit.MILLISECONDS);
    }

    private Runnable getDownloadTask(WebDocument webDocument) {
        return new DownloadTask(webDocument, maximumPdfContentSizeInBytes);
    }


    public static class DownloadTask implements Runnable {

        private WebDocument webDocument;

        private int maximumPdfContentSizeInBytes;

        public DownloadTask(WebDocument webDocument, int maximumPdfContentSizeInBytes) {
            this.webDocument = webDocument;
            this.maximumPdfContentSizeInBytes = maximumPdfContentSizeInBytes;
        }

        @Override
        public void run() {
            downloadSilently();
        }

        public WebDocument downloadSilently() {
            LOGGER.info("Document at url " + webDocument.getUrl() + " is getting downloaded...");
            try {
                download();
            } catch (PdfFileTooBigException | PdfUrlNotValidException | KeyManagementException | NoSuchAlgorithmException e) {
                LOGGER.error("An error occurs while downloading document at url " + webDocument.getUrl() + ".", e);
            }
            return webDocument;
        }

        public void download() throws PdfUrlNotValidException, PdfFileTooBigException, KeyManagementException, NoSuchAlgorithmException {
            initSSLSocketFactory();
            int size;
            try {
                URL url = new URL(webDocument.getUrl());
                URLConnection urlConnection = url.openConnection();
                InputStream inputStream = urlConnection.getInputStream();
                ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
                inputStream.transferTo(outputStream);
                size = outputStream.size();
                if (size > 0 && size < maximumPdfContentSizeInBytes) {
                    webDocument.setPdfContent(outputStream.toByteArray());
                }
                inputStream.close();
                outputStream.close();
            } catch (IOException e) {
                throw new PdfUrlNotValidException(webDocument.getUrl());
            }
            if (size > maximumPdfContentSizeInBytes) {
                throw new PdfFileTooBigException(webDocument.getUrl(), maximumPdfContentSizeInBytes);
            }
            if (size == 0) {
                throw new PdfUrlNotValidException(webDocument.getUrl());
            }
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

    }

    public static class PdfFileTooBigException extends Exception {
        public PdfFileTooBigException(String url, int maximumFileSize) {
            super("The file at url " + url + " exceeds the maximum size configured as " + maximumFileSize + "bytes");
        }
    }

    public static class PdfUrlNotValidException extends Exception {
        public PdfUrlNotValidException(String url, IOException rootException) {
            super("The file at url " + url + " cannot be downloaded, probably because the url is not valid");
        }

        public PdfUrlNotValidException(String url) {
            this(url, null);
        }
    }
}
