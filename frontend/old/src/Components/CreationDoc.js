import React from "react";
import Popup from "reactjs-popup";
import { Breadcrumb, Layout, theme, Button, Form, Input } from "antd";
import CreationEntite from "./CreationEntite";
import { Pages } from "../utils/constants";

const { Header, Content, Footer } = Layout;

function CreationDoc({ compteur, handleCompteurChange }) {
  // Chargement des données JSON depuis un fichier local
  const jsonData = require("../Documents.json");

  // Fonction pour gérer la soumission du formulaire
  const onFinish = (values) => {
    console.log("Success:", values);
    console.log("Ajout de document");
    console.log(JSON.stringify(jsonData, null, 2));
    jsonData.push(values); // Ajout des nouvelles valeurs au JSON
    console.log(JSON.stringify(jsonData, null, 2));
    console.log("Fin ajout de document");
  };

  // Fonction pour gérer l'échec de la soumission du formulaire
  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };

  // Fonction pour gérer le clic sur le bouton de validation
  const handleValidationClick = () => {
    handleCompteurChange(Pages.CREATION_ENTITE);
  };

  // États locaux pour gérer la vue actuelle (document ou entité)
  const [document, setDocument] = React.useState(true);
  const [entity, setEntity] = React.useState(false);

  // Fonction pour afficher la vue de création de document
  const handleDocumentClick = () => {
    setDocument(true);
    setEntity(false);
  };

  // Fonction pour afficher la vue de création d'entité
  const handleEntityClick = () => {
    setDocument(false);
    setEntity(true);
  };

  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  return (
    <Layout>
      <Header
        style={{
          display: "flex",
          alignItems: "center",
        }}
      >
        <div className="demo-logo" />
      </Header>
      <Content
        style={{
          padding: "0 48px",
          minHeight: "100vh",
        }}
      >
        <Breadcrumb
          style={{
            margin: "16px 0",
          }}
        >
          <Breadcrumb.Item>Nom du document</Breadcrumb.Item>
          <Button onClick={handleDocumentClick}>Creation Document</Button>
          <Button onClick={handleEntityClick}>Creation Entity</Button>
        </Breadcrumb>
        <Layout
          style={{
            padding: "24px 0",
            background: colorBgContainer,
            borderRadius: borderRadiusLG,
          }}
        >
          {document ? (
            <Content
              style={{
                padding: "0 24px",
                minHeight: "90vh",
              }}
            >
              <div>
                <h1 className="New_Doc">Nouveau document</h1>
                <div className="Fonction">
                  <br />
                  <Popup
                    style={{ padding: "24px 0px" }}
                    trigger={
                      <Button className="Formulaire">
                        Ajout Formulaire méta-données
                      </Button>
                    }
                  >
                    <Form
                      name="basic"
                      labelCol={{
                        span: 50,
                      }}
                      wrapperCol={{
                        span: 50,
                      }}
                      style={{
                        padding: "0px 300px",
                      }}
                      initialValues={{
                        remember: true,
                      }}
                      onFinish={onFinish}
                      onFinishFailed={onFinishFailed}
                      autoComplete="off"
                    >
                      <Form.Item
                        label="Titre du document"
                        name="document"
                        style={{ padding: "0px 50px" }}
                        rules={[
                          {
                            required: true,
                            message: "Veuillez entrer le titre du document",
                          },
                        ]}
                      >
                        <Input />
                      </Form.Item>
                      <Form.Item
                        label="Date de création"
                        name="date"
                        style={{ padding: "0px 50px" }}
                        rules={[
                          {
                            required: true,
                            message:
                              "Veuillez entrer la date de création du document",
                          },
                        ]}
                      >
                        <Input />
                      </Form.Item>

                      <Form.Item
                        label="Auteur du document"
                        name="auteur"
                        style={{ padding: "0px 50px" }}
                        rules={[
                          {
                            required: true,
                            message: "Veuillez entrer l'auteur du document",
                          },
                        ]}
                      >
                        <Input />
                      </Form.Item>

                      <Form.Item
                        label="Série d'archive du document"
                        name="serie"
                        style={{ padding: "0px 50px" }}
                        rules={[
                          {
                            required: true,
                            message:
                              "Veuillez entrer la série d'archive du document",
                          },
                        ]}
                      >
                        <Input />
                      </Form.Item>

                      <Form.Item
                        label="Type de document"
                        name="type"
                        style={{ padding: "0px 50px" }}
                        rules={[
                          {
                            required: true,
                            message: "Veuillez entrer le type de document",
                          },
                        ]}
                      >
                        <Input />
                      </Form.Item>

                      <Form.Item
                        wrapperCol={{
                          offset: 8,
                          span: 16,
                        }}
                      >
                        <Button type="primary" htmlType="submit">
                          Soumettre
                        </Button>
                      </Form.Item>
                    </Form>
                  </Popup>
                  {/* <Button className="import">Import</Button> */}
                </div>
                <center>
                  <Button
                    onClick={handleValidationClick}
                    className="Validation"
                  >
                    Valider
                  </Button>
                </center>
              </div>
            </Content>
          ) : (
            <CreationEntite
              handleCompteurChange={handleCompteurChange}
              compteur={compteur}
            />
          )}
        </Layout>
      </Content>
      <Footer
        style={{
          textAlign: "center",
        }}
      >
        Ant Design ©{new Date().getFullYear()} Created by Ant UED
      </Footer>
    </Layout>
  );
}

export default CreationDoc;
