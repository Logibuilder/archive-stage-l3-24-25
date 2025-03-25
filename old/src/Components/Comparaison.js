import React, { useState } from "react";

import { Breadcrumb, Layout, theme, Pagination, Button } from "antd";
import { Pages } from "../utils/constants";

const { Header, Content, Footer } = Layout;

function Comparaison({ compteur, handleCompteurChange }) {
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();
  const [selectedComparison, setSelectedComparison] = useState(null);
  const [accuracy, setAccuracy] = useState("");

  const comparisons = [
    { entity1: "Entity 1", entity2: "Entity 36", accuracy: 98 },
    { entity1: "Entity 2", entity2: "Entity 37", accuracy: 85 },
    { entity1: "Entity 3", entity2: "Entity 38", accuracy: 92 },
    // Add more comparisons as needed
  ];

  const handleComparisonClick = (comparison) => {
    setSelectedComparison(comparison);
    setAccuracy(comparison.accuracy);
  };

  const handleAccuracyChange = (e) => {
    setAccuracy(e.target.value);
  };

  const handleModifyClick = () => {
    alert(`Modified accuracy to ${accuracy}%`);
  };

  const handleValidationClick = () => {
    handleCompteurChange(Pages.PROPRIETES);
  };
  const handleRechecheClick = () => {
    handleCompteurChange(Pages.RECHERCHE);
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
        }}
      >
        <Breadcrumb
          style={{
            margin: "16px 0",
          }}
        >
          <Breadcrumb.Item>CreationDoc</Breadcrumb.Item>
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
              minHeight: 280,
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <div style={{ width: "45%" }}>
                <h1 className="wow">Comparisons</h1>
                <br />
                <ul>
                  {comparisons.map((comparison, index) => (
                    <li key={index}>
                      <Button
                        key={index}
                        onClick={() => handleComparisonClick(comparison)}
                      >
                        {comparison.entity1} &gt; {comparison.entity2} (
                        {comparison.accuracy}%)
                      </Button>
                    </li>
                  ))}
                </ul>
                <br />
                <Button onClick={handleValidationClick}>Validate</Button>
              </div>

              <div style={{ width: "45%" }}>
                {selectedComparison ? (
                  <>
                    <h2>Details</h2>
                    <br />
                    <div>
                      <p>Entity 1 : {selectedComparison.entity1}</p>
                      <p>Entity 2 : {selectedComparison.entity2}</p>
                    </div>
                    <div>
                      <label>
                        Accuracy :
                        <input
                          type="number"
                          value={accuracy}
                          onChange={handleAccuracyChange}
                        />
                      </label>
                    </div>
                    <br />
                    <Button onClick={handleModifyClick}> Modify </Button>
                    <Button onClick={handleRechecheClick}>
                      {" "}
                      Recherche SPARQL{" "}
                    </Button>
                  </>
                ) : (
                  <p>Select a comparison to view details.</p>
                )}
              </div>
            </div>
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

export default Comparaison;
