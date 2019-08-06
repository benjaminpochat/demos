import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LocalGovernmentComponent } from './local-government.component';

describe('LocalGovernementComponent', () => {
  let component: LocalGovernmentComponent;
  let fixture: ComponentFixture<LocalGovernmentComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LocalGovernmentComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LocalGovernmentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
