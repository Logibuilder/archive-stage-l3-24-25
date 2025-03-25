import React, { useState } from "react";
import Comparaison from "./Components/Comparaison";
import CreationDoc from "./Components/CreationDoc";
import CreationEntite from "./Components/CreationEntite";
import Home from "./Components/Home";
import Precond from "./Components/Precond";
import Proprietes from "./Components/Proprietes";
import Recherche from "./Components/Recherche";
import Visualisation from "./Components/Visualisation";

import { Pages } from "./utils/constants";

function App() {
  const [compteur, setCompteur] = useState(0);

  return (
    <>
      {
        compteur === Pages.HOME ? (
          <Home handleCompteurChange={setCompteur} compteur={compteur} />
        ) : compteur === Pages.CREATION_DOC ? (
          <CreationDoc handleCompteurChange={setCompteur} compteur={compteur} />
        ) : compteur === Pages.CREATION_ENTITE ? (
          <CreationEntite
            handleCompteurChange={setCompteur}
            compteur={compteur}
          />
        ) : compteur === Pages.COMPARAISON ? (
          <Comparaison handleCompteurChange={setCompteur} compteur={compteur} />
        ) : compteur === Pages.PRECOND ? (
          <Precond handleCompteurChange={setCompteur} compteur={compteur} />
        ) : compteur === Pages.PROPRIETES ? (
          <Proprietes handleCompteurChange={setCompteur} compteur={compteur} />
        ) : compteur === Pages.RECHERCHE ? (
          <Recherche handleCompteurChange={setCompteur} compteur={compteur} />
        ) : compteur === Pages.VISUALISATION ? (
          <Visualisation
            handleCompteurChange={setCompteur}
            compteur={compteur}
          />
        ) : (
          console.log("Erreur de page")
        ) // TODO render a 404 page
      }
    </>
  );
}

export default App;
