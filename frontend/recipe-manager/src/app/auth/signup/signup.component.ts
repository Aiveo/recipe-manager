import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss']
})
export class SignupComponent implements OnInit {

  signupForm: FormGroup;
  errorMessage: string;

  constructor(private formBuilder: FormBuilder,
              private authService: AuthService,
              private router: Router) { }

  ngOnInit() {
    this.initForm();
  }

  initForm() {
    this.signupForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.pattern(/[0-9a-zA-Z]{6,}/)]],
      name: ['', [Validators.required, Validators.pattern(/[a-zA-Z]*/)]],
      surname: ['', [Validators.required, Validators.pattern(/[a-zA-Z]*/)]]
    });
  }

  onSubmit() {
    const email = this.signupForm.get('email').value;
    const password = this.signupForm.get('password').value;
    const lastname = this.signupForm.get('name').value;
    const firstname = this.signupForm.get('surname').value;

    this.authService.signUp(email, password, lastname, firstname).then(
      () => {
        this.router.navigate(['/recipes']);
      },
      (error) => {
        this.errorMessage = error;
      }
    );
  }
}
