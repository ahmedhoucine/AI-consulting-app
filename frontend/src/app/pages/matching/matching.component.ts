import { Component, OnInit, NgZone } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Modal } from 'bootstrap';
import { firstValueFrom } from 'rxjs';

@Component({
  selector: 'app-matching',
  templateUrl: './matching.component.html',
  styleUrls: ['./matching.component.scss']
})
export class MatchingComponent implements OnInit {
  consultants: any[] = [];
  missions: any[] = [];

  selectedConsultant: any | null = null;
  selectedMission: string | null = null;

  recommandation: string = '';
  loading: boolean = false;
  error: string = '';

  emailData = {
    to: '',
    subject: '',
    body: ''
  };

  constructor(private http: HttpClient, private zone: NgZone) {}

   async ngOnInit(): Promise<void> {
  try {
    const data = await firstValueFrom(this.http.get<any[]>('http://localhost:5000/api/advisor/consultants'));
    this.consultants = data;     
    console.log(this.consultants)          
  } catch (error) {
    this.error = 'Erreur de chargement des données';
    console.error('HTTP error:', error);
  }
 
}


  // PARTIE STREAM - NE PAS TOUCHER (comme demandé)
  genererConseilStream(): void {
  if (!this.selectedConsultant?.cv || !this.selectedMission) return;
  console.log(this.selectedConsultant.cv)
  this.recommandation = '';
  this.loading = true;
  this.error = '';

  fetch('http://localhost:5000/api/advisor/stream', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      profile_description: this.selectedConsultant.cv,
      target_job_title: this.selectedMission,
    }),
  })
    .then(response => {
      if (!response.ok) throw new Error('Erreur de réponse du serveur');
      if (!response.body) throw new Error('Corps de réponse vide');

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      const read = () => {
        reader.read().then(({ done, value }) => {
          if (done) {
            this.zone.run(() => (this.loading = false));
            return;
          }

          const text = decoder.decode(value, { stream: true });
          this.zone.run(() => {
            this.recommandation += text;
          });

          read();
        });
      };

      read();
    })
    .catch(error => {
      console.error('Erreur pendant le streaming:', error);
      this.zone.run(() => {
        this.error = 'Erreur lors de la génération du conseil.';
        this.loading = false;
      });
    });
}

  openEmailModal(): void {
    const consultant = this.consultants.find(c => c.id == this.selectedConsultant);
    const mission = this.missions.find(m => m.id == this.selectedMission);

    if (!consultant || !mission) {
      console.error('Consultant ou mission non trouvé');
      return;
    }

    this.emailData.to = consultant.email;
    this.emailData.subject = `Conseils pour le poste ${mission.titre}`;
    this.emailData.body = this.recommandation;

    const modalEl = document.getElementById('emailModal');
    if (modalEl) {
      const modal = new Modal(modalEl);
      modal.show();
    }
  }

  // PARTIE EMAIL - envoi
  envoyerMail(): void {
    this.http.post('http://localhost:5000/api/matching/send-email', this.emailData).subscribe({
      next: () => {
        alert("Email envoyé !");
        const modalEl = document.getElementById('emailModal');
        if (modalEl) {
          const modal = Modal.getInstance(modalEl);
          if (modal) modal.hide();
        }
      },
      error: () => {
        alert("Erreur lors de l'envoi de l'email.");
      }
    });
  }
}
