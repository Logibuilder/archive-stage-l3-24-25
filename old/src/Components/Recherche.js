import React from "react";
import { Breadcrumb, Layout, theme, Pagination, Button } from "antd";
import { Pages } from "../utils/constants";

const { Header, Content, Footer } = Layout;

function Recherche({ compteur, handleCompteurChange }) {
  const handleValidationClick = () => {
    handleCompteurChange(Pages.COMPARAISON);
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
        }}
      >
        <Breadcrumb
          style={{
            margin: "16px 0",
          }}
        >
          <Breadcrumb.Item>Recherche</Breadcrumb.Item>
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
            Recherche SPARQL on est làààà
            <Button onClick={handleValidationClick}>Valider</Button>
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

export default Recherche;
