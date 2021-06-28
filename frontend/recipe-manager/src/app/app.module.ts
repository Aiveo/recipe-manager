import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { SignupComponent } from './auth/signup/signup.component';
import { SigninComponent } from './auth/signin/signin.component';
import { HeaderComponent } from './header/header.component';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {HttpClientModule} from "@angular/common/http";
import {AuthService} from "./services/auth.service";
import {AuthGuardService} from "./services/auth-guard.service";
import { RecipesComponent } from './recipes/recipes.component';
import { SingleRecipeComponent } from './recipes/single-recipe/single-recipe.component';
import { RecipeFormComponent } from './recipes/recipe-form/recipe-form.component';
import {RouterModule, Routes} from "@angular/router";

const appRoutes: Routes = [
  { path: 'auth/signup', component: SignupComponent },
  { path: 'auth/signin', component: SigninComponent },
  { path: 'recipes', component: RecipesComponent },
  { path: 'recipes/new', canActivate: [AuthGuardService], component: RecipeFormComponent },
  { path: 'recipes/:id', component: SingleRecipeComponent },
  { path: 'recipes/user/:id', component: SingleRecipeComponent },
];

@NgModule({
  declarations: [
    AppComponent,
    SignupComponent,
    SigninComponent,
    HeaderComponent,
    RecipesComponent,
    SingleRecipeComponent,
    RecipeFormComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    RouterModule.forRoot(appRoutes)
  ],
  providers: [AuthService, AuthGuardService],
  bootstrap: [AppComponent]
})
export class AppModule { }
