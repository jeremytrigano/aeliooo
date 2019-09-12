import { Component, OnInit } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import {
  FormGroup,
  FormBuilder,
  ReactiveFormsModule,
  Validators
} from "@angular/forms";

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.scss"]
})
export class AppComponent implements OnInit {
  title = "commandes";
  baseUrl: string = "http://localhost:5000";
  commandes: any[];
  public cmdForm: FormGroup;

  constructor(private httpClient: HttpClient, private fb: FormBuilder) {}

  get_commands(nom: string) {
    this.httpClient
      .get(this.baseUrl + "/commandes?nomClient=" + nom)
      .subscribe((res: any[]) => {
        console.log(res);
        this.commandes = res;
      });
  }

  public onSubmit() {
    this.get_commands(this.cmdForm.value.nom);
    console.log(this.cmdForm.value);
  }

  ngOnInit() {
    this.cmdForm = this.fb.group({
      nom: ["", Validators.required],
      adresse: ["", Validators.required]
    });
  }
}
