import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { GlobalStatistics } from '../model/global-statistics.model';

@Injectable()
export class GlobalStatisticsService {

  constructor(private http: HttpClient) {
  }

  public getGlobalStatistics(): Observable<GlobalStatistics> {
      return this.http.get<GlobalStatistics>('http://localhost:8080/scrapingStatistics');
  }
}
