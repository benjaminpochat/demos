import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GlobalStatisticsComponent } from './global-statistics.component';

describe('GlobalStatisticsComponent', () => {
  let component: GlobalStatisticsComponent;
  let fixture: ComponentFixture<GlobalStatisticsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GlobalStatisticsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GlobalStatisticsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
