import SparqlClient from "sparql-http-client";

export const Pages = {
  HOME: 0,
  CREATION_DOC: 1,
  CREATION_ENTITE: 2,
  COMPARAISON: 3,
  PRECOND: 4,
  PROPRIETES: 5,
  RECHERCHE: 6,
  VISUALISATION: 7,
};

export const FUSEKI_ENDPOINT = "http://localhost:3030/DHFC";
export const FUSEKI_CLIENT = new SparqlClient({ endpointUrl: FUSEKI_ENDPOINT+"/query", updateUrl: FUSEKI_ENDPOINT+"/update" });
export const CURRENT_GRAPH = "ComiX";

export const PREFIX = `
  PREFIX dhfc: <http://w3id.org/DHFC#>
`