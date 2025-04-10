import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './index.css'
import Header from './components/Header'
import Ajouter from './components/pages/Ajouter'
import Accueil from './components/pages/Accueil'
import Supprimer from './components/pages/Supprimer'
import Editer from './components/pages/Editer'

function App() {
  return (
    <BrowserRouter>
      <Header />
      <main style={{ padding: '1rem' }}>
        <Routes>
          <Route path="/" element={<Accueil />} />
          <Route path="/ajouter" element={<Ajouter />} />
          <Route path="/supprimer" element={<Supprimer />} />
          <Route path="/editer" element={<Editer />} />
        </Routes>
      </main>
    </BrowserRouter>
  )
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)