import { Component, OnInit } from '@angular/core';
import { FeedbackService } from 'src/app/core/services/feedback';

@Component({
  selector: 'app-basic',
  templateUrl: './basic.component.html',
})
export class BasicComponent implements OnInit {
  feedbacks: any[] = [];

  constructor(private feedbackService: FeedbackService) {}

  ngOnInit(): void {
    this.feedbackService.getFeedbacks().subscribe({
      next: (data) => {
        this.feedbacks = data;
      },
      error: (err) => {
        console.error('Erreur lors de la récupération des feedbacks', err);
      }
    });
  }
}
