import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Subject} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private token = '';
  private endpoint = 'http://0.0.0.0:8080/';
  authSubject = new Subject<boolean>();

  constructor(private httpClient: HttpClient) {}

  isAuth() {
    return this.token !== '';
  }

  emitIsAuth() {
    this.authSubject.next(this.isAuth());
  }

  signUp(email: string, password: string, name: string, surname: string) {
    return new Promise<void>(
      (resolve, reject) => {
        this.httpClient
          .post(this.endpoint + 'register?' +
            'email=' + email +
            '&password=' + password +
            '&name=' + name +
            '&surname=' + surname,
            {})
          .subscribe(
            (response: any) => {
              this.token = response.token;
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
          .post(this.endpoint + 'login?e'+
            'mail=' + email +
            '&password=' + password,
            {})
          .subscribe(
            (response: any) => {
              this.token = response.token;
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
    this.emitIsAuth();
  }
}
