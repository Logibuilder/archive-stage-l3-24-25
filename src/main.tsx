import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './index.css'
import Header from './components/Header'

// Placeholder pages
const placeholder = (name: string) => {
  console.log(`Navigate to: ${name}`);
  return <h1>{name}</h1>;
}

function App() {
  return (
    <BrowserRouter>
      <Header />
      <main style={{ padding: '1rem' }}>
        <Routes>
          <Route path="/" element={placeholder('Interface DHFC')} />
          <Route path="/ajouter" element={placeholder('Ajouter')} />
          <Route path="/supprimer" element={placeholder('Supprimer')} />
          <Route path="/editer" element={placeholder('Éditer')} />
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