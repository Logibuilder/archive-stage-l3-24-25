import { FUSEKI_CLIENT, PREFIX } from "./constants";

export function getDocuments() {
  const query =
    PREFIX +
    `
        SELECT ?document WHERE {
            ?document a dhfc:Document
        }
    `;

  return FUSEKI_CLIENT.get(query).then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response;
  });
}
