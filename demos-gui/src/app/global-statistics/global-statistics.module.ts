import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GlobalStatisticsComponent } from './components/global-statistics.component';
import { GlobalStatisticsService } from './services/global-statistics.service';
import { HttpClient, HttpHandler, HttpClientModule } from '@angular/common/http';

@NgModule({
  declarations: [
    GlobalStatisticsComponent
  ],
  imports: [
    CommonModule,
    HttpClientModule
  ],
  exports: [
    GlobalStatisticsComponent
  ],
  providers: [
    GlobalStatisticsService
  ]
})
export class GlobalStatisticsModule { }
