import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RestablecerContra } from './restablecer-contra';

describe('RestablecerContra', () => {
  let component: RestablecerContra;
  let fixture: ComponentFixture<RestablecerContra>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RestablecerContra]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RestablecerContra);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
