package org.demos.pdfconverter.process;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.commons.codec.digest.DigestUtils;
import org.apache.kafka.common.errors.SerializationException;
import org.apache.kafka.common.serialization.Deserializer;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.common.serialization.Serializer;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.Consumed;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.Produced;
import org.demos.pdfconverter.model.WebDocument;

import java.util.Properties;

public class PdfConversionStreamProcessor {
    public static void main(String[] args) {
        new PdfConversionStreamProcessor().process(args);
    }

    private void process(String[] args){
        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "pdf-converter");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        Serde<WebDocument> webDocumentSerde = Serdes.serdeFrom(new UnclassifiedWebDocumentSerializer(), new UnclassifierWebDocumentDeserializer());

        StreamsBuilder builder = new StreamsBuilder();
        PdfConverter converter = new PdfConverter();

        // stream d'entrée
        KStream<String, WebDocument> pdfUrlStream = builder.stream("UnclassifiedPdfUrl", Consumed.with(Serdes.String(), webDocumentSerde));

        KStream<String, WebDocument> webDocumentStream = pdfUrlStream.mapValues(converter::convert)
                .filter((url, webDocument) -> webDocument.getTextContent() != null)
                .mapValues(this::generateId);
        webDocumentStream.to("UnclassifiedPdfContent", Produced.with(Serdes.String(), webDocumentSerde));

        KafkaStreams streams = new KafkaStreams(builder.build(), props);
        streams.start();
    }

    private WebDocument generateId(WebDocument webDocument) {
        webDocument.setId(DigestUtils.sha256Hex(webDocument.getTextContent()));
        return webDocument;
    }

    private class UnclassifiedWebDocumentSerializer implements Serializer<WebDocument> {
        private final ObjectMapper objectMapper = new ObjectMapper();

        @Override
        public byte[] serialize(String topic, WebDocument unclassifiedWebDocument) {
            if (unclassifiedWebDocument == null) {
                return null;
            }
            try {
                return objectMapper.writeValueAsBytes(unclassifiedWebDocument);
            } catch (JsonProcessingException e) {
                throw new SerializationException("Error serializing JSON message", e);
            }
        }
    }

    private class UnclassifierWebDocumentDeserializer implements Deserializer<WebDocument> {
        private final ObjectMapper objectMapper = new ObjectMapper();

        @Override
        public WebDocument deserialize(String topic, byte[] bytes) {
            if (bytes == null)
                return null;

            WebDocument data;
            try {
                data = objectMapper.readValue(bytes, WebDocument.class);
            } catch (Exception e) {
                throw new SerializationException("Error deserializing JSON message", e);
            }

            return data;
        }
    }


}
