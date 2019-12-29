package org.demos.pdfconverter.process;

import org.apache.pdfbox.cos.COSDocument;
import org.apache.pdfbox.io.RandomAccessBuffer;
import org.apache.pdfbox.io.RandomAccessRead;
import org.apache.pdfbox.pdfparser.PDFParser;
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

public class PdfConverter {

    static Logger LOGGER = LoggerFactory.getLogger(PdfConverter.class);

    public WebDocument convert(WebDocument webDocument) {
        LOGGER.info("url " + webDocument.getUrl() + " is getting converted...");
        String parsedText = null;
        try{
            initSSLSocketFactory();
            URL url = new URL(webDocument.getUrl());
            URLConnection urlConnection = url.openConnection();
            InputStream inputStream = urlConnection.getInputStream();
            PDDocument pDDocument = getPDDocument(inputStream);
            PDFTextStripper pdfStripper = new PDFTextStripper();
            parsedText = pdfStripper.getText(pDDocument);
            pDDocument.close();
        } catch (Throwable t){
            LOGGER.error("An error occurs while converting " + webDocument.getUrl() + " into text.", t);
        }
        webDocument.setTextContent(parsedText);
        return webDocument;
    }

    PDDocument getPDDocument(InputStream inputStream) throws IOException {
        RandomAccessRead randomAccessRead = new RandomAccessBuffer(inputStream);
        PDFParser parser = new PDFParser(randomAccessRead);
        parser.parse();
        COSDocument cosDoc = parser.getDocument();
        return new PDDocument(cosDoc);
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
