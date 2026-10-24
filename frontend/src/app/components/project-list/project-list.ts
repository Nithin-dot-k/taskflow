import { Component, OnInit, signal } from '@angular/core';
import { ProjectService } from '../../services/project';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-project-list',
  imports: [CommonModule, RouterLink],
  standalone: true,
  templateUrl: './project-list.html',
  styleUrl: './project-list.css',
})
export class ProjectList implements OnInit {
  projects = signal<any[]>([]);

  constructor(
    private projectService: ProjectService,
    private router: Router,
  ) {}

  // OnInit is a special Angular method that runs automatically
  // the moment this page is loaded.
  ngOnInit() {
    if (!localStorage.getItem('token')) {
      this.router.navigate(['/login']);
      return;
    }

    this.projectService.getProjects().subscribe({
      next: (data) => {
        this.projects.set(data);
      },
      error: (err) => {
        console.error('Error fetching projects:', err);
        // If the backend says the token is invalid or expired:
        if (err.status === 401) {
          localStorage.removeItem('token'); // Clear the bad token
          this.router.navigate(['/login']); // Redirect to login
        }
      },
    });
  }
}
