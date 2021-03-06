import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { LocalGovernment } from '../model/local-government.model';
import { WebDocument } from 'src/app/web-document/model/web-document.model';
import { environment } from 'src/environments/environment';

@Injectable()
export class LocalGovernmentService {

  constructor(private http: HttpClient) {
  }

  public searchLocalGovernments(name: string): Observable<Array<LocalGovernment>> {
      return this.http.get<Array<LocalGovernment>>(environment.demosCoreUrl + '/localGovernments/searchByName/' + name);
  }

  public getWebDocuments(localGovernment: LocalGovernment): Observable<Array<WebDocument>> {
    return this.http.get<Array<WebDocument>>(environment.demosCoreUrl + '/localGovernments/' + localGovernment.id + '/webDocuments');
  }

  public loadLocalGovernment(localGovernment: LocalGovernment): Observable<LocalGovernment> {
    return this.http.get<LocalGovernment>(environment.demosCoreUrl + '/localGovernments/' + localGovernment.id);
  }
}
