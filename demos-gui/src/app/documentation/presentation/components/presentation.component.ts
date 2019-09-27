import { Component } from '@angular/core';
import { trigger, state, style, animate, transition, keyframes } from '@angular/animations';

@Component({
  selector: 'app-presentation',
  templateUrl: './presentation.component.html',
  styleUrls: ['./presentation.component.css'],
  animations: [
    trigger('displayHide', [
      state('displayed', style({})),
      state('hidden', style({display: 'none'})),
      transition('displayed => hidden', [
        animate(
          '300ms',
          keyframes([
            style({ opacity: 0 })
        ]))
      ]),
      transition('hidden => displayed', [
        animate(
          '300ms',
          keyframes([
            style({ display: 'block', opacity: 0}),
            style({ opacity: 1 }),
        ]))
      ])
    ]),
  ],
})

export class PresentationComponent {

  isDisplayed = false;

  toggle() {
    this.isDisplayed = !this.isDisplayed;
  }
}
