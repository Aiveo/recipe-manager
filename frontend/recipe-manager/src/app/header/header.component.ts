import { Component, OnInit } from '@angular/core';
import {AuthService} from "../services/auth.service";
import {Subscription} from "rxjs";

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {

  isAuth: boolean;
  isAuthSubscribtion: Subscription;

  constructor(private authService: AuthService) { }

  ngOnInit(): void {
    this.isAuthSubscribtion= this.authService.authSubject.subscribe(
      (isAuth: boolean) => {
        this.isAuth = isAuth;
      }
    );
    this.authService.emitIsAuth();
  }

  onSignOut() {
    this.authService.signOut();
  }
}
