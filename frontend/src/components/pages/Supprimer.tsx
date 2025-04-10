import { useState } from 'react';
import { getDocuments } from "../../utils";
import { DHFC_Document } from '../../types';

export default function Supprimer() {
    const [selectedDocument, setSelectedDocument] = useState<DHFC_Document | null>(null);
    const documents = getDocuments();
    
    const handleDocumentChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        const selectedId = event.target.value;
        if (selectedId) {
            const document = documents.find(doc => doc.id === selectedId);
            setSelectedDocument(document!);
        } else {
            setSelectedDocument(null);
        }
    };
    
    const handleDelete = () => {
        alert(`Suppression de ${selectedDocument!.metadata.name} : ${selectedDocument!.metadata.author}`);
    };

    return (
        <div>
            <h1>Supprimer</h1>
            
            <div>
                <label htmlFor="document-select">
                    Sélectionner un document:
                </label>
                <select 
                    id="document-select"
                    onChange={handleDocumentChange}
                    value={selectedDocument?.id || ""}
                >
                    <option value="">-- Sélectionner un document --</option>
                    {documents.map(doc => (
                        <option key={doc.id} value={doc.id}>
                            {doc.metadata.name} : {doc.metadata.author}
                        </option>
                    ))}
                </select>
            </div>
            
            {selectedDocument && (
                <div>
                    <h2>Document sélectionné:</h2>
                    <p>{JSON.stringify(selectedDocument)}</p>
                </div>
            )}
            
            <button
                disabled={!selectedDocument}
                onClick={handleDelete}
            >
                Supprimer
            </button>
        </div>
    );
}