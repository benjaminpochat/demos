import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LocalGovernmentSelectorComponent } from './local-government-selector.component';

describe('LocalGovernmentSelectorComponent', () => {
  let component: LocalGovernmentSelectorComponent;
  let fixture: ComponentFixture<LocalGovernmentSelectorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LocalGovernmentSelectorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LocalGovernmentSelectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
