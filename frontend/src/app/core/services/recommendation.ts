import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, switchMap, forkJoin } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class RecommendationService {
  constructor(private http: HttpClient) {}

  getRecommendations(consultantId: number): Observable<any[]> {
    return this.http.get<any>(`http://localhost:5002/api/consultants/${consultantId}`).pipe(
      switchMap((consultant) => {
        const cv = consultant.cv;
        const payload = { query: cv };
        return this.http.post<any>('http://localhost:5002/recommend', payload);
      }),
      switchMap((response: any) => {
        console.log('Response from /recommend:', response);

        const jobIds = response.recommendations;

        if (!Array.isArray(jobIds)) {
          throw new Error('Expected an array of job IDs from /recommend');
        }

        const jobRequests = jobIds.map((id: number) =>
          this.http.get<any>(`http://localhost:5002/api/jobs/${id}`)
        );

        return forkJoin(jobRequests);
      })
    );
  }

  getConsultants(): Observable<any[]> {
    return this.http.get<any[]>(`http://localhost:5002/api/consultants`);
  }
}
