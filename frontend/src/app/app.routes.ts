import { Routes } from '@angular/router';

import { PaginaPrin } from './pagina-prin/pagina-prin';
import { Login } from './login/login';
import { RecuperarContra } from './recuperar-contra/recuperar-contra';
import { Register } from './register/register';
import { RestablecerContra } from './restablecer-contra/restablecer-contra';
import { Admin } from './admin/admin';
import { Carrito } from './carrito/carrito';
import { ApartadoPrin } from './apartado-prin/apartado-prin';

export const routes: Routes = [
  { path: '', component: PaginaPrin }, // Ruta principal (inicio)
  { path: 'login', component: Login },
  { path: 'recuperar-contra', component: RecuperarContra },
  { path: 'register', component: Register },
  { path: 'restablecer-contra', component: RestablecerContra },
  { path: 'admin', component: Admin },
  { path: 'carrito', component: Carrito},
  {path: 'apartado-prin', component: ApartadoPrin}
];
