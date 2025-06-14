import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ApartadoPrin } from './apartado-prin';

describe('ApartadoPrin', () => {
  let component: ApartadoPrin;
  let fixture: ComponentFixture<ApartadoPrin>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ApartadoPrin]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ApartadoPrin);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
