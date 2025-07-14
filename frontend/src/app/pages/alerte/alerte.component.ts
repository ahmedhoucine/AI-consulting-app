import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import Swal from 'sweetalert2';

interface Alerte {
  id: number;
  nom_prenom: string;
  nbr_jrs_inactifs: number;
  date_derniere_mission: string | null;
  action_recommandee: string;
}

@Component({
  selector: 'app-alerte',
  templateUrl: './alerte.component.html',
})
export class AlerteComponent implements OnInit {
  alertes: Alerte[] = [];
  loading = false;

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.chargerAlertes();
  }

  chargerAlertes() {
    this.http.get<Alerte[]>('http://localhost:5000//api/alerte/alertes').subscribe(data => {
      this.alertes = data;
    });
  }

  

  supprimerAlerte(alerte: Alerte) {
    const swalWithBootstrapButtons = Swal.mixin({
      customClass: {
        confirmButton: 'btn btn-success',
        cancelButton: 'btn btn-danger ms-2'
      },
      buttonsStyling: false
    });

    swalWithBootstrapButtons
      .fire({
        title: 'Êtes-vous sûr ?',
        text: 'Cette alerte sera supprimée définitivement.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Oui, supprimer !',
        cancelButtonText: 'Non, annuler !'
      })
      .then(result => {
        if (result.isConfirmed) {
          this.http.delete(`http://localhost:5000/api/alerte/${alerte.id}/delete`).subscribe(() => {
            this.alertes = this.alertes.filter(a => a.id !== alerte.id);

            swalWithBootstrapButtons.fire(
              'Supprimée !',
              'L\'alerte a été supprimée.',
              'success'
            );
          });
        } else if (result.dismiss === Swal.DismissReason.cancel) {
          swalWithBootstrapButtons.fire(
            'Annulé',
            'L\'alerte est toujours là :)',
            'error'
          );
        }
      });
  }
}
