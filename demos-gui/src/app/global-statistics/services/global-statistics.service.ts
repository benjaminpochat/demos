import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { GlobalStatistics } from '../model/global-statistics.model';
import { environment } from 'src/environments/environment';

@Injectable()
export class GlobalStatisticsService {

  constructor(private http: HttpClient) {
  }

  public getGlobalStatistics(): Observable<GlobalStatistics> {
      return this.http.get<GlobalStatistics>(environment.demosCoreUrl + '/scrapingStatistics');
  }
}
