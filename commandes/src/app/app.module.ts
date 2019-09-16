import { BrowserModule } from "@angular/platform-browser";
import { NgModule } from "@angular/core";
import { HttpClientModule } from "@angular/common/http";
import { AppRoutingModule } from "./app-routing.module";
import { AppComponent } from "./app.component";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { LivreurComponent } from "./livreur/livreur.component";
import { RouterModule, Routes } from "@angular/router";
import { ClientComponent } from "./client/client.component";

const appRoutes: Routes = [
  { path: "", component: ClientComponent },
  { path: "liv", component: LivreurComponent, runGuardsAndResolvers: "always" }
];
@NgModule({
  declarations: [AppComponent, LivreurComponent, ClientComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    RouterModule.forRoot(appRoutes, { onSameUrlNavigation: "reload" })
  ],
  providers: [],
  bootstrap: [AppComponent],
  exports: [RouterModule]
})
export class AppModule {}
