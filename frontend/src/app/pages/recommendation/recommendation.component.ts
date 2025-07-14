import { Component, OnInit } from '@angular/core';
import { firstValueFrom } from 'rxjs';
import { RecommendationService } from 'src/app/core/services/recommendation';

@Component({
  selector: 'app-recommendation',
  templateUrl: './recommendation.component.html'
})
export class RecommendationComponent implements OnInit {
  consultants: any[] = [];
  selectedConsultantId: number | null = null;
  recommendations: any[] = [];
  loading = false;

  constructor(private recommendationService: RecommendationService) {}

  ngOnInit() {
    this.recommendationService.getConsultants().subscribe(data => {
      this.consultants = data;
    });
  }

  async onConsultantChange() {
  if (this.selectedConsultantId) {
    this.loading = true;

    try {
      this.recommendations = await firstValueFrom(
        this.recommendationService.getRecommendations(this.selectedConsultantId)
      );

      console.log(this.recommendations);
    } catch (error) {
      console.error('Failed to fetch recommendations', error);
    } finally {
      this.loading = false;
      console.log("from finally", this.recommendations);
    }
  }
}

}
