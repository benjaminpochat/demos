import { TestBed } from '@angular/core/testing';

import { GlobalStatisticsService } from './global-statistics.service';

describe('GlobalStatisticsService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: GlobalStatisticsService = TestBed.get(GlobalStatisticsService);
    expect(service).toBeTruthy();
  });
});
