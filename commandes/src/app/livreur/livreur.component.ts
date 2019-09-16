import { Component, OnInit } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import { ActivatedRoute, Router } from "@angular/router";

@Component({
  selector: "app-livreur",
  templateUrl: "./livreur.component.html",
  styleUrls: ["./livreur.component.scss"]
})
export class LivreurComponent implements OnInit {
  title = "commandes";
  baseUrl: string = "http://localhost:5000";
  commandes: any[];
  public cmdForm: FormGroup;
  private commande: any[];

  constructor(
    private httpClient: HttpClient,
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  get_commands() {
    this.httpClient
      .get(this.baseUrl + "/commandes/livreur")
      .subscribe((res: any[]) => {
        console.log("res");
        console.log(res);
        this.commandes = res;
      });
  }

  ngOnInit() {
    this.cmdForm = this.fb.group({
      nom: ["", Validators.required],
      adresse: ["", Validators.required]
    });
    this.httpClient
      .get(this.baseUrl + "/commandes/livreur")
      .subscribe((res: any[]) => {
        this.commandes = res;
      });
  }

  public onSubmitLiv(id: number, etat: number) {
    this.commande = [
      {
        id: id,
        etat: etat
      }
    ];
    this.httpClient
      .put(this.baseUrl + "/commandes", this.commande)
      .subscribe((res: any[]) => {
        this.commandes = res;
      });
    this.router.navigate(["liv"]);
  }
}
