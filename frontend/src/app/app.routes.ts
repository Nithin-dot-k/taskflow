import { Routes } from '@angular/router';
import { SignupComponent } from './components/signup/signup.component';
import { Login } from './components/login/login';

export const routes: Routes = [
    { path: 'signup', component: SignupComponent },
    { path: 'login', component: Login }
];
