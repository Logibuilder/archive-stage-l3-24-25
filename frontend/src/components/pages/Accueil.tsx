import { useNavigate } from 'react-router-dom';

export default function Accueil(): React.ReactElement {
    const navigate = useNavigate();
    
    return (
        <div>
            <h1>Accueil</h1>
            <p>Historien, vous qui entrez, abandonnez tout espoir.</p>
            <p style={{ fontSize: '0.8rem' }}>(Texte temporaire je savais pas quoi mettre)</p>

            <button onClick={() => navigate('/dashboard')}>
                Entrer
            </button>
        </div>
    );
}