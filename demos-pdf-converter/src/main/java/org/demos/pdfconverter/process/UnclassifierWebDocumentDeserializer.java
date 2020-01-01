package org.demos.pdfconverter.process;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.common.errors.SerializationException;
import org.apache.kafka.common.serialization.Deserializer;
import org.demos.pdfconverter.model.WebDocument;

class UnclassifierWebDocumentDeserializer implements Deserializer<WebDocument> {
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
