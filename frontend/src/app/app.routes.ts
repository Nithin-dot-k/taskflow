import { Routes } from '@angular/router';
import { SignupComponent } from './components/signup/signup.component';
import { Login } from './components/login/login';
import { ProjectList } from './components/project-list/project-list';
import { CreateProject } from './components/create-project/create-project';


export const routes: Routes = [
  { path: 'signup', component: SignupComponent },
  { path: 'login', component: Login },
  { path: 'projects', component: ProjectList },
  { path: 'create-project', component: CreateProject },
];
