import { Component, OnInit } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";

@Component({
  selector: "app-client",
  templateUrl: "./client.component.html",
  styleUrls: ["./client.component.scss"]
})
export class ClientComponent implements OnInit {
  title = "commandes";
  baseUrl: string = "http://localhost:5000";
  public commandes: any;
  public cmdFormRech: FormGroup;
  public cmdFormPass: FormGroup;
  private commande: any[];

  constructor(private httpClient: HttpClient, private fb: FormBuilder) {}

  get_commands(nom: string) {
    this.httpClient
      .get(this.baseUrl + "/commandes?nomClient=" + nom)
      .subscribe((res: any[]) => {
        this.commandes = res;
      });
  }

  pass_commands(nom: string, adresse: string) {
    this.commande = [
      {
        nom: nom,
        adresse: adresse
      }
    ];
    this.httpClient
      .post(this.baseUrl + "/commandes", this.commande)
      .subscribe((res: any[]) => {
        this.commandes = res;
      });
  }

  public onSubmitRech() {
    this.get_commands(this.cmdFormRech.value.nom);
  }

  public onSubmitPass() {
    this.pass_commands(
      this.cmdFormPass.value.nom,
      this.cmdFormPass.value.adresse
    );
  }

  ngOnInit() {
    this.commandes = [];
    this.cmdFormRech = this.fb.group({
      nom: ["", Validators.required],
      adresse: ["", Validators.required]
    });
    this.cmdFormPass = this.fb.group({
      nom: ["", Validators.required],
      adresse: ["", Validators.required]
    });
  }
}
