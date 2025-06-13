import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PaginaPrin } from './pagina-prin';

describe('PaginaPrin', () => {
  let component: PaginaPrin;
  let fixture: ComponentFixture<PaginaPrin>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PaginaPrin]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PaginaPrin);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
