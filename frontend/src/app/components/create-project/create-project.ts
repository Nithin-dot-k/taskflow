import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ProjectService } from '../../services/project';
import { Router } from '@angular/router';

@Component({
  selector: 'app-create-project',
  imports: [FormsModule],
  standalone: true,
  templateUrl: './create-project.html',
  styleUrl: './create-project.css',
})
export class CreateProject implements OnInit {
  title = '';
  description = '';

  constructor(private projectService: ProjectService,private router: Router) {}

  ngOnInit() {
    const token = localStorage.getItem('token');
    if (!token) {
      this.router.navigate(['/login']); // Redirect if no token found!
    }
  }

  onCreate() {
    const newProject = { title: this.title, description: this.description };
    this.projectService.createProject(newProject).subscribe({
      next: () => {
        alert("Project created!");
        this.router.navigate(['/projects']);
      },
      error: (err) => alert("Error creating project")
    });
  }
}
