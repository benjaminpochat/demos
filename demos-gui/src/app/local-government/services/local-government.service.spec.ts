import { TestBed } from '@angular/core/testing';

import { LocalGovernmentService } from './local-government.service';

describe('LocalGovernmentServiceService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: LocalGovernmentService = TestBed.get(LocalGovernmentService);
    expect(service).toBeTruthy();
  });
});
