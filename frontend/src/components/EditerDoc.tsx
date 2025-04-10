import { useState } from 'react';
import { DHFC_Document } from '../types';
import { default_document, default_entity } from '../utils';


export default function EditerDoc({doc, onFinish}: {doc: DHFC_Document, onFinish: (doc: DHFC_Document) => void}) {
    const [activeTab, setActiveTab] = useState<'metadata' | 'content'>('metadata');
    const [documentData, setDocumentData] = useState<DHFC_Document>(doc);

    // Handle input changes
    const handleInputChange = (tab: 'metadata' | 'content', field: string, value: string) => {
        setDocumentData(prev => ({
            ...prev,
            [tab]: {
                ...prev[tab],
                [field]: value
            }
        }));
    };

    // Check if all fields are filled
    const isFormComplete = () => {
        const { metadata, content } = documentData;
        return (
            metadata.name.trim() !== '' &&
            metadata.author.trim() !== '' &&
            metadata.date !== null &&
            content.entities.length > 0 &&
            content.entities.every(entity => entity.type.trim() !== '' && entity.data !== null && entity.data.trim() !== '')
        );
    };

    const handleEntityInputChange = (idx: number, field: string, value: string) => {
        setDocumentData(prev => ({
            ...prev,
            content: {
                ...prev.content,
                entities: prev.content.entities.map((entity, index) =>
                    index === idx ? { ...entity, [field]: value } : entity
                )
            }
        }));
    }

    // Handle form submission
    const handleAddDocument = () => {
        onFinish(documentData);

        // Reset form
        setDocumentData(default_document());
        setActiveTab('metadata');
    };

    const entityForm = (entity_idx: number) => {
        const entity = documentData.content.entities[entity_idx]
        return (
            <div>
                <div>
                    <label htmlFor="type">Type :</label>
                    <input
                        id="type"
                        type="text"
                        value={entity.type}
                        onChange={(e) => handleEntityInputChange(entity_idx, 'type', e.target.value)}
                    />
                </div>

                <div>
                    <label htmlFor="data">Données :</label>
                    <input
                        id="data"
                        type="text"
                        value={entity.data || ''}
                        onChange={(e) => handleEntityInputChange(entity_idx, 'data', e.target.value)}
                    />
                </div>
            </div>
        )
    }

    const addEntity = () => {
        setDocumentData(prev => ({
            ...prev,
            content: {
                ...prev.content,
                entities: [...prev.content.entities, default_entity()]
            }
        }));
    }

    return (
        <div>
            <div>
                <button onClick={() => setActiveTab('metadata')}>
                    Métadonnées
                </button>
                <button onClick={() => setActiveTab('content')}>
                    Contenu
                </button>
            </div>

            {activeTab === 'metadata' && (
                <div>
                    <div>
                        <label htmlFor="name">Nom :</label>
                        <input
                            id="name"
                            type="text"
                            value={documentData.metadata.name}
                            onChange={(e) => handleInputChange('metadata', 'name', e.target.value)}
                        />
                    </div>

                    <div>
                        <label htmlFor="author">Auteur :</label>
                        <input
                            id="author"
                            type="text"
                            value={documentData.metadata.author}
                            onChange={(e) => handleInputChange('metadata', 'author', e.target.value)}
                        />
                    </div>

                    <div>
                        <label htmlFor="date">Date :</label>
                        <input
                            id="date"
                            type="date"
                            value={documentData.metadata.date instanceof Date
                                ? documentData.metadata.date.toISOString().split('T')[0]
                                : documentData.metadata.date || ''}
                            onChange={(e) => handleInputChange('metadata', 'date', e.target.value)}
                        />
                    </div>
                </div>)
            }

            {activeTab === 'content' && (
                <div>
                    <div>
                        {documentData.content.entities.map((_, index) => (
                            <>
                                <p>---------</p>
                                <div key={index}>
                                    {entityForm(index)}
                                </div>
                            </>
                        ))}
                    </div>
                    <button
                        onClick={() => {
                            addEntity();
                        }}
                    >
                        Ajouter une entité
                    </button>
                </div>
            )}

            <button
                disabled={!isFormComplete()}
                onClick={handleAddDocument}
            >
                Confirmer
            </button>
        </div>
    );
}