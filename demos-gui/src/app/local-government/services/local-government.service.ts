import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { LocalGovernment } from '../model/local-government.model';
import { WebDocument } from 'src/app/web-document/model/web-document.model';

@Injectable()
export class LocalGovernmentService {

  constructor(private http: HttpClient) {
  }

  public searchLocalGovernments(name: string): Observable<Array<LocalGovernment>> {
      return this.http.get<Array<LocalGovernment>>('http://localhost:8080/localGovernments/searchByName/' + name);
  }

  public getWebDocuments(localGovernment: LocalGovernment): Observable<Array<WebDocument>> {
    return this.http.get<Array<WebDocument>>('http://localhost:8080/localGovernments/' + localGovernment.id + '/webDocuments');
  }
}
