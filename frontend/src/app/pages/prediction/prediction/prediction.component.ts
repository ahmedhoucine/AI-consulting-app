import { Component, OnInit } from '@angular/core';
import { PredictionService } from 'src/app/core/services/prediction.service';

@Component({
  selector: 'app-prediction',
  templateUrl: './prediction.component.html',
  styleUrls: ['./prediction.component.scss']
})
export class PredictionComponent implements OnInit {
  predictions: any = {};
  months: string[] = [];
  selectedMonth: string = '';

  clusteredTitleChart: any;
  secteurChart: any;
  bubbleChartOption: any;

  constructor(private predictionService: PredictionService) {}

  ngOnInit(): void {
    this.predictionService.getPredictions().subscribe((res) => {
      this.predictions = res.data;
      this.months = Object.keys(this.predictions['clustered_title']);
      if (this.months.length > 0) {
        this.selectedMonth = this.months[0];
        this.updateCharts();
      }
    });
  }

  updateCharts(): void {
    const titles = this.predictions["clustered_title"][this.selectedMonth];
    const skills = this.predictions["skills"][this.selectedMonth];
    const secteurs = this.predictions["secteur"][this.selectedMonth];

    // Classement titres - Barre horizontale
    this.clusteredTitleChart = {
      series: [{
        data: titles.map((_, i) => 10 - i) // 10 à 1 (Top 1 = 10)
      }],
      chart: {
        type: "bar",
        height: 400
      },
      xaxis: {
        categories: titles.map(t => t.label),
        title: { text: 'Titres classés (Top 10)' }
      },
      yaxis: {
        title: { text: 'Rang (Top 1 en haut)' }
      },
      colors: ['#556ee6'],
      dataLabels: {
        enabled: false
      },
     
    };

    // Skills - Bubble Chart (sans score, avec taille basée sur le rang inversé)
    this.bubbleChartOption = {
      tooltip: {
        trigger: 'item',
        formatter: function (param) {
          return `${param.data[3]} (Top ${param.data[4]})`;
        }
      },
      xAxis: { name: 'Index', type: 'value' },
      yAxis: { name: 'Classement', type: 'value', inverse: true },
      series: [{
        name: 'Compétences',
        type: 'scatter',
        data: skills.map((s, i) => [i, i + 1, (10 - i) * 4, s.label, i + 1]),
        symbolSize: function (data) { return data[2]; },
        emphasis: {
          label: {
            show: true,
            formatter: function (param) {
              return `${param.data[3]} (Top ${param.data[4]})`;
            },
            position: 'top'
          }
        },
        itemStyle: {
          color: '#34c38f',
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.2)',
          shadowOffsetY: 5
        }
      }],
      title: { text: `Compétences – Classement ${this.selectedMonth}` }
    };

    // Secteurs - Donut Chart avec libellés Top X uniquement
    this.secteurChart = {
      series: new Array(secteurs.length).fill(1), // égalité entre tous
      chart: {
        type: "donut",
        height: 400
      },
      labels: secteurs.map((s, i) => `Top ${i + 1} – ${s.label}`),
      legend: {
        position: 'bottom'
      },
      title: { text: `Secteurs – Classement ${this.selectedMonth}` },
      colors: ['#f46a6a', '#556ee6', '#f1b44c', '#34c38f', '#50a5f1', '#343a40', '#ff7f50', '#9370db', '#20c997', '#ff69b4']
    };
  }
}
