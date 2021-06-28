import { Component, OnInit } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-single-recipe',
  templateUrl: './single-recipe.component.html',
  styleUrls: ['./single-recipe.component.scss']
})
export class SingleRecipeComponent implements OnInit {

  private endpoint = 'http://localhost:8080/';

  recipe: object = {
    "id":0,
    "name":null,
    "preparation_time":0,
    "cooking_time":0,
    "description":null,
    "image":null,
    "portion":0,
    "id_user":0,
    "firstname":null,
    "lastname":null,
    "steps":null,
    "ingredients":null
  };

  constructor(private httpClient: HttpClient, private route: ActivatedRoute) {
  }

  ngOnInit(): void {
    const id = this.route.snapshot.params['id'];
    this.getRecipe(id);
  }

  getRecipe(id: number) {
    return new Promise<void>(
      (resolve, reject) => {
        this.httpClient
          .get(this.endpoint + 'getOneRecipe?' +
            'id=' + id,
            {})
          .subscribe(
            (response: any) => {
              this.recipe = response;
              console.log(this.recipe);
              resolve();
            },
            (error) => {
              reject(error.error.detail);
            }
          );
      }
    );
  }
}
