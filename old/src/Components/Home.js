import React, { useState, useEffect } from "react";
import { Breadcrumb, Layout, theme, Button, Form, Input } from "antd"; // Ajout de l'import Input
import Popup from "reactjs-popup";
import { FUSEKI_CLIENT, Pages } from "../utils/constants";
import { getDocuments } from "../utils/functions";

const { Header, Content, Footer } = Layout;

function Accueil({handleCompteurChange, setVisualisation }) {
  const [allDocs, setAllDocs] = useState([]);
  const [loadingDocs, setLoadingDocs] = useState(true);
  const [errorDocs, setErrorDocs] = useState(null);
  const [selectedDocument, setselectedDocument] = useState(null);

  useEffect(() => {
    getDocuments()
      .then((data) => {
        setAllDocs(data);
        setLoadingDocs(false);
      })
      .catch((error) => {
        setErrorDocs(error);
        setLoadingDocs(false);
      });
  }, []);

  if (loadingDocs) {
    return <div>Loading...</div>;
  }
  if (errorDocs) {
    return <div>Error: {errorDocs.message}</div>;
  }
  console.log("allDocs", allDocs);

  // Fonction pour gérer le clic sur un document
  const handleDocumentClick = (document) => {
    console.log(document);
    setselectedDocument(document);
  };


  // TODO : Connecter à Fuseki sur le serveur
  const documents = [
    {
      name: "Ordonnance de Monseigneur de Toulouse",
      type: "Type A",
      properties: ["Property 1", "Property 2"],
    },
    {
      name: "Ordonnance Royale",
      type: "Type B",
      properties: ["Property 3", "Property 4"],
    },
  ];

  // Fonction pour gérer le clic sur le bouton d'ajout
  const handleAjoutclick = () => {
    handleCompteurChange(Pages.CREATION_DOC);
  };

  // Fonction pour gérer le clic sur le bouton de visualisation
  const handleVisualisationClick = () => {
    setVisualisation(true);
  };

  // Fonction de gestion de la soumission du formulaire
  const onFinish = (values) => {
    selectedDocument.name = values.document;
    selectedDocument.type = values.type;
    selectedDocument.properties = Object.values(values).slice(2);
    console.log("Success:", selectedDocument);
    console.log("Modification des valeurs");
  };

  // Fonction de gestion de l'échec de la soumission du formulaire
  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };

  return (
    <>
      <div style={{ height: "100%", justifyContent: "space-between" }}></div>
      <div>
        <Button onClick={() => handleAjoutclick()}>
          <div className="text-4xl">+</div>
          <div className="ml-2">Ajouter document</div>
        </Button>
        <br />
        <div className="Document-list">
          {documents.map((document, index) => (
            <div className="doc" key={index}>
              <div className="doc-header">
                <Button onClick={() => handleDocumentClick(document)}>
                  {document.name}
                </Button>
              </div>
              <br />
            </div>
          ))}
        </div>
      </div>

      <div style={{ width: "45%" }}>
        {selectedDocument ? (
          <>
            <h2>Détails</h2>
            <br />
            <div>
              <p>Nom du document : {selectedDocument.name}</p>
              <p>Type de document : {selectedDocument.type}</p>
              <p>
                Propriétés du document :
                {selectedDocument.properties.map((properties, index) => (
                  <p key={index}>- {properties}</p>
                ))}
              </p>
            </div>
            <div>
              <Popup trigger={<Button>Modifier les valeurs</Button>}>
                <Form
                  name="basic"
                  style={{
                    padding: "0px 500px",
                  }}
                  initialValues={{
                    remember: false,
                  }}
                  onFinish={onFinish}
                  onFinishFailed={onFinishFailed}
                  autoComplete="off"
                >
                  <Form.Item
                    label="Titre du document"
                    name="document"
                    style={{ padding: "0px 1000px" }}
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
                    label="Type"
                    name="type"
                    style={{ padding: "0px 1000px" }}
                    rules={[
                      {
                        required: true,
                        message: "Veuillez entrer le type du document",
                      },
                    ]}
                  >
                    <Input />
                  </Form.Item>
                  {selectedDocument.properties.map((properties, index) => (
                    <Form.Item
                      label={index}
                      name={properties}
                      style={{ padding: "0px 1000px" }}
                      rules={[
                        {
                          required: true,
                          message: "Veuillez entrer la valeur",
                        },
                      ]}
                    >
                      <Input />
                    </Form.Item>
                  ))}
                  <Form.Item
                    wrapperCol={{
                      offset: 8,
                      span: 16,
                    }}
                    style={{ padding: "0px 1000px" }}
                  >
                    <Button type="primary" htmlType="submit">
                      Soumettre
                    </Button>
                  </Form.Item>
                </Form>
              </Popup>
            </div>
            <br />
            <Button onClick={handleVisualisationClick}>
              Visualisation du graphe
            </Button>
          </>
        ) : (
          <p>Cliquez sur un document pour connaître ses informations</p>
        )}
      </div>
    </>
  );
}

function Home({ compteur, handleCompteurChange }) {
  const [Visualisation, setVisualisation] = useState(false);
  const [MesDocument, setMesDocument] = useState(true);
  const [MaSynthese, setMaSynthese] = useState(false);

  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  // Fonction pour gérer le clic sur le bouton de visualisation totale
  const handleTotalVisuClick = () => {
    alert("Visualisation totale du graphe de connaissance");
  };

  // Fonction pour gérer le clic sur le bouton "Mes documents"
  const handleMesDocumentClick = () => {
    setMesDocument(true);
    setMaSynthese(false);
  };

  // Fonction pour gérer le clic sur le bouton "Ma synthèse"
  const handleMaSyntheseClick = () => {
    setMesDocument(false);
    setMaSynthese(true);
  };

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
          display: "-ms-flexbox",
          minHeight: "100vh",
        }}
      >
        <Breadcrumb
          style={{
            margin: "16px 0",
          }}
        >
          <Breadcrumb.Item>Accueil</Breadcrumb.Item>
          <Button onClick={handleMesDocumentClick}>Mes documents</Button>
          <Button onClick={handleMaSyntheseClick}>Ma synthèse</Button>
        </Breadcrumb>
        <Layout
          style={{
            padding: "24px 0",
            background: colorBgContainer,
            borderRadius: borderRadiusLG,
          }}
        >
          <Content
            style={{
              padding: "0 24px",
              minHeight: "90vh",
            }}
          >
            {MesDocument ? (
              <div style={{ display: "ms-grid" }}>
                <div>
                  <Accueil
                    handleCompteurChange={handleCompteurChange}
                    setVisualisation={setVisualisation}
                  />
                  <br />
                  <Button onClick={handleTotalVisuClick}>
                    Visualisation totale du graphe de connaissance
                  </Button>
                </div>
                <br />
                <div>
                  {Visualisation ? (
                    <div style={{ padding: "-10px 900px" }}>
                      Visualisation du graphe on est lààà
                    </div>
                  ) : null}
                </div>
              </div>
            ) : (
              <div>Ma synthèse</div>
            )}
          </Content>
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

export default Home;
