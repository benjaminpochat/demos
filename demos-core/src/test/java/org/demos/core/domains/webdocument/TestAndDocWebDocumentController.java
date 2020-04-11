package org.demos.core.domains.webdocument;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.restdocs.RestDocumentationContextProvider;
import org.springframework.restdocs.RestDocumentationExtension;
import org.springframework.test.context.jdbc.Sql;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.context.WebApplicationContext;

import static org.springframework.restdocs.mockmvc.MockMvcRestDocumentation.document;
import static org.springframework.restdocs.mockmvc.MockMvcRestDocumentation.documentationConfiguration;
import static org.springframework.restdocs.mockmvc.RestDocumentationRequestBuilders.get;
import static org.springframework.restdocs.operation.preprocess.Preprocessors.*;
import static org.springframework.restdocs.payload.PayloadDocumentation.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@ExtendWith({RestDocumentationExtension.class, SpringExtension.class})
@Transactional
@Sql({"/org/demos/core/domains/webdocument/TestWebDocumentController.sql"})
public class TestAndDocWebDocumentController {
    private MockMvc mockMvc;

    @BeforeEach
    public void setUp(WebApplicationContext webApplicationContext,
                      RestDocumentationContextProvider restDocumentation) {
        this.mockMvc = MockMvcBuilders.webAppContextSetup(webApplicationContext)
                .apply(documentationConfiguration(restDocumentation))
                .build();
    }

    @Test
    public void getWebDocument() throws Exception {
        this.mockMvc
                .perform(get("/webDocuments/dec9441d673a08fecbacb386a16553d8675a6765"))
                .andExpect(status().isOk())
                .andDo(document(
                        "get-webDocument",
                        preprocessRequest(prettyPrint()),
                        preprocessResponse(prettyPrint()),
                        responseFields(
                                fieldWithPath("id").description("The demos id of the web document (sha-1 function result of the web document text content)"),
                                fieldWithPath("url").description("The url where the document is located in the web"),
                                fieldWithPath("textContent").description("The text content of the document"),
                                subsectionWithPath("localGovernment").description("The local government associated with the web document")
                        )));
    }

    @Test
    public void getWebDocuments() throws Exception {
        this.mockMvc
                .perform(get("/webDocuments"))
                .andExpect(status().isOk())
                .andDo(document(
                        "get-webDocuments",
                        preprocessRequest(prettyPrint()),
                        preprocessResponse(prettyPrint())));
    }

    @Test
    public void createWebDocument() throws Exception {
        this.mockMvc
                .perform(post("/webDocuments")
                        .contentType(MediaType.APPLICATION_JSON_UTF8)
                        .content("{\n" +
                        "  \"id\" : \"13d3d34dc82681f6fd76dd787bab3bb42c8030db\",\n" +
                        "  \"url\" : \"https://www.bechy.fr/CR_2020_12_03.pdf\",\n" +
                        "  \"localGovernment\" : {\n" +
                        "    \"id\" : 101\n" +
                        "  },\n" +
                        "  \"textContent\" : \"Le conseil municipal a décidé de ...\"\n" +
                        "}"))
                .andExpect(status().isOk())
                .andDo(document(
                        "create-webDocument",
                        preprocessRequest(prettyPrint()),
                        preprocessResponse(prettyPrint())));
    }

}
