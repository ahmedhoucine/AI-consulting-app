import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-page-title',
  templateUrl: './pagetitle.component.html',
  styleUrls: ['./pagetitle.component.scss']
})
export class PagetitleComponent implements OnInit {

  @Input() title: string;
  @Input() breadcrumbItems: Array<{ label: string; path: string; active?: boolean }>;


  constructor() { }

  ngOnInit() {
  }

}
