import React from 'react';
import { useNavigate } from 'react-router-dom';

// Style

const headerStyle: React.CSSProperties = {
    backgroundColor: 'black',
    color: 'white',
    padding: '1rem',
    display: 'flex',
    justifyContent: 'space-between',
};

const buttonStyle: React.CSSProperties = {
    background: 'none',
    border: 'none',
    padding: 0,
    color: 'white',
    textDecoration: 'none',
    cursor: 'pointer',
    font: 'inherit',
    marginRight: '1rem',
};

// Component

export default function Header(): React.ReactElement {
    const navigate = useNavigate();

    const buttonNavigation = (text: string, path: string) => {
        return (
            <button style={buttonStyle} onClick={() => navigate(path)}>
                {text}
            </button>
        );
    };

    return (
        <header style={headerStyle}>
            <div>
                {buttonNavigation('Interface DHFC', '/')}
            </div>
            <div>
                {buttonNavigation('Ajouter', '/ajouter')}
                {buttonNavigation('Supprimer', '/supprimer')}
                {buttonNavigation('Éditer', '/editer')}
            </div>
        </header>
    );
};