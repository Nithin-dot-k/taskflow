import { Routes } from '@angular/router';
import { SignupComponent } from './components/signup/signup.component';
import { Login } from './components/login/login';
import { ProjectList } from './components/project-list/project-list';
import { CreateProject } from './components/create-project/create-project';
import { ProjectDetail } from './components/project-detail/project-detail';
import { authGuard } from './services/auth-guard';


export const routes: Routes = [
  { path: 'signup', component: SignupComponent },
  { path: 'login', component: Login },
  { path: 'projects', component: ProjectList, canActivate: [authGuard] },
  { path: 'create-project', component: CreateProject, canActivate: [authGuard] },
  { path: 'projects/:id', component: ProjectDetail, canActivate: [authGuard] },
  { path: '', redirectTo: 'login', pathMatch: 'full' }
];
