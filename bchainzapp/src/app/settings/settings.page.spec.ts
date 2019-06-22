import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Settings } from './settings.page';

describe('Tab3Page', () => {
  let component: Settings;
  let fixture: ComponentFixture<Settings>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [Settings],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Settings);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
