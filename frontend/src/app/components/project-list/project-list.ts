import { Component, OnInit, signal } from '@angular/core';
import { ProjectService } from '../../services/project';

@Component({
  selector: 'app-project-list',
  imports: [],
  standalone: true,
  templateUrl: './project-list.html',
  styleUrl: './project-list.css',
})
export class ProjectList implements OnInit {
  projects = signal<any[]>([]); 

  constructor(private projectService: ProjectService) {}

  // OnInit is a special Angular method that runs automatically
  // the moment this page is loaded.
  ngOnInit() {
    this.projectService.getProjects().subscribe({
      next: (data) => {
        this.projects.set(data); // Update the signal with the new data
        // console.log('projects:', this.projects); // Add this log!
      },
      error: (err) => console.error('Error:', err),
    });
  }
}
