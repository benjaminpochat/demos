package org.demos.core.domains.localgovernment;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.boot.test.context.SpringBootTest;
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
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@ExtendWith({RestDocumentationExtension.class, SpringExtension.class})
@Transactional
@Sql({"/org/demos/core/domains/localgovernment/TestLocalGovernmentController.sql"})
public class TestAndDocLocalGovernmentController {

    private MockMvc mockMvc;

    @BeforeEach
    public void setUp(WebApplicationContext webApplicationContext,
                      RestDocumentationContextProvider restDocumentation) {
        this.mockMvc = MockMvcBuilders.webAppContextSetup(webApplicationContext)
                .apply(documentationConfiguration(restDocumentation))
                .build();
    }

    @Test
    public void getLocalGovernments() throws Exception {
        this.mockMvc
                .perform(get("/localGovernments/101"))
                .andExpect(status().isOk())
                .andDo(document(
                        "get-localGovernments",
                        preprocessRequest(prettyPrint()),
                        preprocessResponse(prettyPrint()),
                        responseFields(
                                fieldWithPath("id").description("The demos id of the local government"),
                                fieldWithPath("name").description("The name of the local government"),
                                fieldWithPath("type").description("The type of local government"),
                                fieldWithPath("webSite").description("The website url of the local government"),
                                fieldWithPath("latitude").description("The latitude of the local government's geographic localization"),
                                fieldWithPath("longitude").description("The longitude of the local government's geographic localization"),
                                fieldWithPath("codification").description("An identifier of the local government, prefixed with the codification's descriptor"),
                                fieldWithPath("zipCode").description("The zip code of the local government"),
                                subsectionWithPath("overlappingLocalGovernments").description("The list of other local governments that govern the same place, from higher levels"))));
    }

    @Test
    public void searchLocalGovernmentByName() throws Exception {
        this.mockMvc
                .perform(get("/localGovernments/searchByName/Po"))
                .andExpect(status().isOk())
                .andDo(document(
                        "search-localGovernments",
                        preprocessRequest(prettyPrint()),
                        preprocessResponse(prettyPrint())));
    }

    @Test
    public void getLocalGovernmentByWebSite() throws Exception {
        this.mockMvc
                .perform(get("/localGovernments").param("webSite", "www.bethune.fr"))
                .andExpect(status().isOk())
                .andDo(document(
                        "get-localGovernment-by-webSite",
                        preprocessRequest(prettyPrint()),
                        preprocessResponse(prettyPrint())));

    }

    @Test
    public void getWebDocumentsByLocalGovernment() throws Exception {
        this.mockMvc
                .perform(get("/localGovernments/101/webDocuments"))
                .andExpect(status().isOk())
                .andDo(document(
                        "get-webDocuments-by-localGovernemnt",
                        preprocessRequest(prettyPrint()),
                        preprocessResponse(prettyPrint())));

    }

}
