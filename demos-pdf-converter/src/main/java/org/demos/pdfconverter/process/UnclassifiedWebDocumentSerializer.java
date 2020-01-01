package org.demos.pdfconverter.process;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.common.errors.SerializationException;
import org.apache.kafka.common.serialization.Serializer;
import org.demos.pdfconverter.model.WebDocument;

class UnclassifiedWebDocumentSerializer implements Serializer<WebDocument> {
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
