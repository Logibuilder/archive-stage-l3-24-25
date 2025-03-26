import React, { useState } from "react";
import { Breadcrumb, Layout, theme, Button } from "antd";
import Precond from "./Precond";
import { Pages } from "../utils/constants";

const { Header, Content, Footer } = Layout;

function CreationEntite({ compteur, handleCompteurChange }) {
  // Utilisation du hook pour obtenir les tokens de thème
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  // État pour les entités
  const [entities, setEntities] = useState([
    {
      name: "Entity 1",
      type: "Type A",
      properties: ["Property 1", "Property 2"],
    },
    {
      name: "Entity 2",
      type: "Type B",
      properties: ["Property 3", "Property 4"],
    },
  ]);

  // État pour l'index de l'entité sélectionnée
  const [selectedEntityIndex, setSelectedEntityIndex] = useState(null);
  // État pour la condition préalable
  const [precond, setPrecond] = useState(false);

  // Fonction pour ajouter une nouvelle entité
  const handleAddEntity = () => {
    const newEntity = {
      name: "New Entity",
      type: "New Type",
      properties: ["New Property"],
    };
    setEntities([...entities, newEntity]);
    setSelectedEntityIndex(entities.length); // Sélectionner la nouvelle entité ajoutée
    setPrecond(true);
  };

  // Fonction pour mettre à jour une entité
  const handleEntityUpdate = (updatedEntity, index) => {
    const updatedEntities = entities.map((entity, i) =>
      i === index ? updatedEntity : entity,
    );
    setEntities(updatedEntities);
  };

  // Fonction pour gérer la soumission du formulaire
  const handleSubmit = () => {
    console.log("Form submitted");
    handleCompteurChange(Pages.COMPARAISON);
  };

  // Fonction pour gérer la sélection d'une entité
  const handleSelectedClick = (index) => {
    setSelectedEntityIndex(index);
    setPrecond(true);
  };

  return (
    <Content style={{ padding: "0 24px", minHeight: "100vh" }}>
      <div className="container">
        <h1 className="title">Affirmation de document</h1>
        <div className="actions">
          <Button className="action-button" onClick={handleAddEntity}>
            <span className="plus">+</span>
            Nouvelle Entité
          </Button>
        </div>
        <center>
          <br />
          <div className="entity-list" style={{ display: "flex" }}>
            {entities.map((entity, index) => (
              <div className="entity" key={index}>
                <Button
                  style={{ display: "block" }}
                  onClick={() => handleSelectedClick(index)}
                >
                  <div className="entity-header">
                    <span>{entity.name}</span>
                    <span>{entity.type}</span>
                  </div>
                  {selectedEntityIndex === index && (
                    <>
                      <br />
                      <div className="entity-properties">
                        {entity.properties.map((property, idx) => (
                          <div key={idx}>{property}</div>
                        ))}
                      </div>
                      <br />
                    </>
                  )}
                </Button>
              </div>
            ))}
          </div>
          <br />
          <Button className="validate-button" onClick={handleSubmit}>
            Valider
          </Button>
          <br />
          <br />
          <br />
          <br />
          <br />
          <br />
          <br />
          <br />
        </center>
        {precond && selectedEntityIndex !== null ? (
          <Precond
            handleCompteurChange={handleCompteurChange}
            compteur={compteur}
            entity={entities[selectedEntityIndex]}
            handleEntityUpdate={(updatedEntity) =>
              handleEntityUpdate(updatedEntity, selectedEntityIndex)
            }
          />
        ) : null}
      </div>
    </Content>
  );
}

export default CreationEntite;
