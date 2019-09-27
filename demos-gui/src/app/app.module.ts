import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { LocalGovernmentModule } from './local-government/local-government.module';
import { GlobalStatisticsModule } from './global-statistics/global-statistics.module';
import { WebDocumentModule } from './web-document/web-document.module';
import { DocumentationModule } from './documentation/documentation.module';

@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    GlobalStatisticsModule,
    LocalGovernmentModule,
    WebDocumentModule,
    DocumentationModule
  ],

  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
