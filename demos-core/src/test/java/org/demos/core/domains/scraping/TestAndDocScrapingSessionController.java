package org.demos.core.domains.scraping;

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
import static org.springframework.restdocs.mockmvc.RestDocumentationRequestBuilders.put;
import static org.springframework.restdocs.operation.preprocess.Preprocessors.*;
import static org.springframework.restdocs.payload.PayloadDocumentation.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@ExtendWith({RestDocumentationExtension.class, SpringExtension.class})
@Transactional
@Sql({"/org/demos/core/domains/scraping/TestScrapingSessionController.sql"})
public class TestAndDocScrapingSessionController {

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
                .perform(get("/scrapingSessions"))
                .andExpect(status().isOk())
                .andDo(document(
                        "get-next-scrapingSession",
                        preprocessRequest(prettyPrint()),
                        preprocessResponse(prettyPrint()),
                        responseFields(
                                fieldWithPath("id").description("The demos id of the scraping session returned"),
                                fieldWithPath("creation").description("The creation date-time of the scraping session"),
                                fieldWithPath("endScraping").description("The date-time when the scraping process end for this session"),
                                subsectionWithPath("localGovernment").description("The local government associated with the scraping session"))));
    }

    @Test
    public void updateLocalGovernments() throws Exception {
        this.mockMvc
                .perform(
                        put("/scrapingSessions")
                                .contentType(MediaType.APPLICATION_JSON_UTF8)
                                .content("{\n" +
                                        "  \"id\" : 1,\n" +
                                        "  \"creation\" : \"2020-04-11T18:23:18.497501\",\n" +
                                        "  \"endScraping\" : \"2020-04-11T19:00:00.000000\"\n" +
                                        "}"))
                .andExpect(status().isOk())
                .andDo(document(
                        "update-scrapingSession",
                        preprocessRequest(prettyPrint()),
                        preprocessResponse(prettyPrint())));
    }
}
