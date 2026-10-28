import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router'; 
import { TaskService } from '../../services/task';

@Component({
  selector: 'app-project-detail',
  imports: [CommonModule, FormsModule],
  standalone: true,
  templateUrl: './project-detail.html',
  styleUrl: './project-detail.css',
})
export class ProjectDetail implements OnInit {
   // Store the project ID extracted from the URL
  projectId!: number;

  // Signal holding the list of tasks for this project
  tasks = signal<any[]>([]);

  // Form input variables for creating a new task
  newTaskTitle = '';
  newTaskDescription = '';

  constructor(
    private route: ActivatedRoute,    // Inject the URL Scanner
    private taskService: TaskService,  // Inject the Task API Service
    private router: Router,   
  ) {}

  ngOnInit() {
    // 1. Read the ':id' parameter from the active route
    const idParam = this.route.snapshot.paramMap.get('id');
    this.projectId = Number(idParam);

    // 2. Automatically load the tasks for this project
    this.loadTasks();
  }

  loadTasks() {
    this.taskService.getTasks(this.projectId).subscribe({
      next: (data) => {
        this.tasks.set(data);
      },
      error: (err) => { console.error('Error fetching tasks:', err);
      // If project does not exist or user is unauthorized:
        if (err.status === 403 || err.status === 404) {
          alert("Project not found or you don't have permission to access it.");
          this.router.navigate(['/projects']); // Kick them back to safety!
        }
      }
    });
  }

  onAddTask() {
    if (!this.newTaskTitle.trim()) {
      alert('Please enter a task title');
      return;
    }

    // Notice: we attach this.projectId automatically!
    const payload = {
      title: this.newTaskTitle,
      description: this.newTaskDescription,
      project_id: this.projectId
    };

    this.taskService.createTask(payload).subscribe({
      next: (createdTask) => {
        // Clear the form
        this.newTaskTitle = '';
        this.newTaskDescription = '';
        // Refresh the tasks list on the screen
        this.loadTasks();
      },
      error: (err) => console.error('Error creating task:', err)
    });
  }

   // --- NEW: Helper to filter tasks by status for each column ---
  getTasksByStatus(status: string) {
    return this.tasks().filter(task => task.status === status);
  }

  // --- NEW: Method to update task status ---
  onMoveStatus(taskId: number, nextStatus: string) {
    this.taskService.updateTaskStatus(taskId, nextStatus).subscribe({
      next: () => {
        this.loadTasks(); // Refresh the board so the card hops to its new column!
      },
      error: (err) => console.error('Error updating task status:', err)
    });
  }
}
