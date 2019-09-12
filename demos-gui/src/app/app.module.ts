import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { LocalGovernmentModule } from './local-government/local-government.module';
import { GlobalStatisticsModule } from './global-statistics/global-statistics.module';
import { WebDocumentModule } from './web-document/web-document.module';

@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    GlobalStatisticsModule,
    LocalGovernmentModule,
    WebDocumentModule
  ],

  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
