import React, { useState, useEffect } from "react";
import { Button, theme, Layout } from "antd"; // Ajuster les imports selon votre configuration
import { Pages } from "../utils/constants";

const { Header, Content, Footer } = Layout;

function Precond({
  compteur,
  handleCompteurChange,
  entity,
  handleEntityUpdate,
}) {
  // Utilisation du hook pour obtenir les tokens de thème
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  // États pour le nom, l'option sélectionnée et les propriétés
  const [name, setName] = useState("");
  const [selectedOption, setSelectedOption] = useState("");
  const [properties, setProperties] = useState([]);

  // Hook pour mettre à jour les états lorsque l'entité change
  useEffect(() => {
    if (entity) {
      setName(entity.name);
      setSelectedOption(entity.type);
      setProperties(
        entity.properties.map((prop, idx) => ({
          name: `Property ${idx + 1}`,
          value: prop,
        })),
      );
    }
  }, [entity]);

  // Gestion du changement de nom
  const handleNameChange = (e) => {
    setName(e.target.value);
  };

  // Gestion du changement d'option
  const handleOptionChange = (e) => {
    setSelectedOption(e.target.value);
  };

  // Gestion de la validation des modifications
  const handleValidationClick = () => {
    const updatedEntity = {
      name,
      type: selectedOption,
      properties: properties.map((prop) => prop.value),
    };
    handleEntityUpdate(updatedEntity);
    handleCompteurChange(Pages.CREATION_ENTITE);
  };

  // Gestion de l'ajout d'une nouvelle propriété
  const handleAddProperty = () => {
    const newProperty = {
      name: `Property ${properties.length + 1}`,
      value: "",
    };
    setProperties([...properties, newProperty]);
  };

  // Gestion de la suppression d'une propriété
  const handleDeleteProperty = (index) => {
    const newProperties = properties.filter((_, i) => i !== index);
    setProperties(newProperties);
  };

  // Gestion du changement de valeur d'une propriété
  const handlePropertyChange = (index, newValue) => {
    const newProperties = properties.map((property, i) =>
      i === index ? { ...property, value: newValue } : property,
    );
    setProperties(newProperties);
  };

  return (
    <Content style={{ padding: "0 24px", minHeight: 280 }}>
      <div className="container">
        <h1 className="title">Nouvelle Entité</h1>
        <div className="form-group">
          <label className="label" htmlFor="name">
            Nom :{" "}
          </label>
          <input
            className="input"
            id="name"
            type="text"
            value={name}
            onChange={handleNameChange}
          />
        </div>
        <div className="form-group">
          <label className="label" htmlFor="dropdown">
            Options :{" "}
          </label>
          <select
            className="select"
            id="dropdown"
            value={selectedOption}
            onChange={handleOptionChange}
          >
            <option value="" disabled>
              Select an option
            </option>
            <option value="Option 1">Option 1</option>
            <option value="Option 2">Option 2</option>
            <option value="Option 3">Option 3</option>
          </select>
        </div>
        <center>
          <table className="sheet">
            <thead>
              <tr>
                <th>Propriété</th>
                <th>Valeur</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {properties.map((property, index) => (
                <tr key={index}>
                  <td>{property.name}</td>
                  <td>
                    <input
                      type="text"
                      value={property.value}
                      onChange={(e) =>
                        handlePropertyChange(index, e.target.value)
                      }
                    />
                  </td>
                  <td>
                    <Button onClick={() => handleDeleteProperty(index)}>
                      -
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <br />
          <Button onClick={handleAddProperty}>+</Button>
          <br />
          <Button onClick={handleValidationClick} className="validate-button">
            Valider
          </Button>
        </center>
      </div>
    </Content>
  );
}

export default Precond;
