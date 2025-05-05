import { useState } from 'react';
import { DHFC_Document, DHFC_Entity } from '../../types';
import { default_document, default_entity } from '../../utils';
import EditEntity, { isEntityValid } from './EditEntity';

export default function EditerDoc({ doc, onFinish }: { doc: DHFC_Document, onFinish: (doc: DHFC_Document) => void }) {
    const [activeTab, setActiveTab] = useState<'metadata' | 'content'>('metadata');
    const [documentData, setDocumentData] = useState<DHFC_Document>(doc);

    // Handle input changes
    const handleMetadataInputChange = (field: string, value: string) => {
        setDocumentData(prev => ({
            ...prev,
            metadata: {
                ...prev.metadata,
                [field]: value
            }
        }));
    };

    const isFormComplete = () => {
        const { metadata, entities } = documentData;
        return (
            metadata.name.trim() !== '' &&
            metadata.author.trim() !== '' &&
            metadata.date !== null &&
            entities.length > 0 &&
            entities.every(entity => isEntityValid(entity))
        );
    };

    const handleEntityInputChange = (idx: number) => (entity: DHFC_Entity) => {
        setDocumentData(prev => ({
            ...prev,
            entities: prev.entities.map((e, index) =>
                index === idx ? entity : e
            )
        }));
    }

    // Handle form submission
    const handleAddDocument = () => {
        onFinish(documentData);

        // Reset form
        setDocumentData(default_document());
        setActiveTab('metadata');
    };

    const addEntity = () => {
        setDocumentData(prev => ({
            ...prev,
            entities: [...prev.entities, default_entity()]
        }
        ));
    }

    const deleteEntity = (index: number) => {
        setDocumentData(prev => ({
            ...prev,
            entities: prev.entities.filter((_, i) => i !== index)
        }));
    };

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
                            onChange={(e) => handleMetadataInputChange('name', e.target.value)}
                        />
                    </div>

                    <div>
                        <label htmlFor="author">Auteur :</label>
                        <input
                            id="author"
                            type="text"
                            value={documentData.metadata.author}
                            onChange={(e) => handleMetadataInputChange('author', e.target.value)}
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
                            onChange={(e) => handleMetadataInputChange('date', e.target.value)}
                        />
                    </div>
                </div>)
            }

            {activeTab === 'content' && (
                <div>
                    <div>
                        {documentData.entities.map((_, index) => (
                            <>
                                <p>---------</p>
                                <div key={index}>
                                    # edit entity component
                                    <EditEntity
                                        entity={documentData.entities[index]}
                                        onChange={handleEntityInputChange(index)}
                                        onSuppr={() => deleteEntity(index)}
                                    />
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