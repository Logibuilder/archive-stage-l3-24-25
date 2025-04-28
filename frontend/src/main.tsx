import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './index.css'
import Header from './components/Header'
import Ajouter from './components/pages/Ajouter'
import Accueil from './components/pages/Accueil'
import Editer from './components/pages/Editer'
import { Dashboard } from './components/pages/Dashboard'
import { Voir } from './components/pages/Voir'
import { DocumentProvider } from './components/DocumentProvider'

function App() {
  return (
    <DocumentProvider>
      <BrowserRouter>
        <Header />
        <main style={{ padding: '1rem' }}>
          <Routes>
            <Route path="/" element={<Accueil />} />
            <Route path="/ajouter" element={<Ajouter />} />
            <Route path="/editer" element={<Editer />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/voir" element={<Voir />} />
          </Routes>
        </main>
      </BrowserRouter>
    </DocumentProvider>
  )
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)