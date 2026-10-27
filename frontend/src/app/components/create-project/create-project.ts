import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ProjectService } from '../../services/project';
import { Router } from '@angular/router';

@Component({
  selector: 'app-create-project',
  imports: [FormsModule, CommonModule],
  standalone: true,
  templateUrl: './create-project.html',
  styleUrl: './create-project.css',
})
export class CreateProject {
  title = '';
  description = '';

  constructor(private projectService: ProjectService,private router: Router) {}

  onCreate() {
    if (!this.title.trim()) {
      alert("Please provide a project title.");
      return;
    }
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
