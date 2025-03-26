import React from "react";
import { Layout, Button } from "antd";
import { Pages } from "../utils/constants";

const { Content } = Layout;

function Visualisation({ compteur, handleCompteurChange }) {
  const handleReturnClick = () => {
    handleCompteurChange(Pages.HOME);
  };
  return (
    <Content
      style={{
        padding: "0 24px",
        minHeight: 280,
      }}
    >
      Visualisation du graphe on est làààà
      <Button onClick={handleReturnClick}>Bouton retour</Button>
    </Content>
  );
}

export default Visualisation;
