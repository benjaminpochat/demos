import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { WebDocumentListComponent } from './web-document-list.component';

describe('WebDocumentListComponent', () => {
  let component: WebDocumentListComponent;
  let fixture: ComponentFixture<WebDocumentListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ WebDocumentListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(WebDocumentListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
