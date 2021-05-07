import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Subject} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private token = '';
  private endpoint = 'http://localhost:8080/';
  authSubject = new Subject<boolean>();

  constructor(private httpClient: HttpClient) {
    if(localStorage.getItem("token")) {
      this.token = localStorage.getItem("token");
    }
  }

  isAuth() {
    return this.token !== '';
  }

  emitIsAuth() {
    this.authSubject.next(this.isAuth());
  }

  signUp(email: string, password: string, lastname: string, firstname: string) {
    return new Promise<void>(
      (resolve, reject) => {
        this.httpClient
          .post(this.endpoint + 'register?' +
            'email=' + email +
            '&password=' + password +
            '&lastname=' + lastname +
            '&firstname=' + firstname,
            {})
          .subscribe(
            (response: any) => {
              this.token = response.token;
              localStorage.setItem("token", this.token);
              this.emitIsAuth();
              resolve();
            },
            (error) => {
              reject(error.error.detail);
            }
          );
      }
    );
  }

  signIn(email: string, password: string) {
    return new Promise<void>(
      (resolve, reject) => {
        this.httpClient
          .post(this.endpoint + 'login?'+
            'email=' + email +
            '&password=' + password,
            {})
          .subscribe(
            (response: any) => {
              this.token = response.token;
              localStorage.setItem("token", this.token);
              this.emitIsAuth();
              resolve();
            },
            (error) => {
              reject(error.error.detail);
            }
          );
      }
    );
  }

  signOut() {
    this.token = '';
    localStorage.removeItem("token");
    this.emitIsAuth();
  }
}
