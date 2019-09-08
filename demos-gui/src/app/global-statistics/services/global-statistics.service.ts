import { Injectable } from '@angular/core';
import { GlobalStatistics } from '../model/global-statistics.model';
import { HttpClient, HttpRequest, HttpInterceptor, HttpHandler, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable()
export class GlobalStatisticsService {

  constructor(private http: HttpClient) {
  }

  public getGlobalStatistics<T>(): Observable<any> {
      return this.http.get('http://localhost:8080/scrapingStatistics');
  }

}

// @Injectable()
// export class CustomInterceptor implements HttpInterceptor {

//     intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
//         if (!req.headers.has('Content-Type')) {
//             req = req.clone({ headers: req.headers.set('Content-Type', 'application/json') });
//         }

//         req = req.clone({ headers: req.headers.set('Accept', 'application/json') });
//         return next.handle(req);
//     }
// }
