import { createContext, useCallback, useContext, useState, ReactNode, useEffect } from 'react';
import { DHFC_Document } from '../types';
import config from '../config';

// Create the context with a default value
interface DocumentContextType {
    documents: Record<string, DHFC_Document>;
    loading: boolean;
    error: string | null;
    addDocument: (document: DHFC_Document) => Promise<void>;
    deleteDocument: (document: DHFC_Document) => Promise<void>;
}

const DocumentContext = createContext<DocumentContextType | undefined>(undefined);

export function DocumentProvider({ children }: { children: ReactNode }) {
    const [documents, setDocuments] = useState<Record<string, DHFC_Document>>({});
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // get documents
    useEffect(() => {
        (async () => {
            try {

                const response = await fetch(`${config.API_URL}/documents`);
                if (!response.ok) {
                    throw new Error("Erreur lors de la récupération des documents");
                }
                setDocuments(await response.json());

            } catch (err) {
                setError(err as string);
            } finally {
                setLoading(false);
            }
        })();
    }, []);

    const addDocument = useCallback(async (document: DHFC_Document) => {
        try {

            const response = await fetch(`${config.API_URL}/documents`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(document),
            });

            if (!response.ok) {
                throw new Error("Erreur lors de l'ajout du document");
            }

            setDocuments(prev => ({
                ...prev,
                [document.id]: document
            }));
        } catch (err) {
            setError(err as string);
        } finally {
            setLoading(false);
        }
    }, []);

    const deleteDocument = useCallback(async (doc: DHFC_Document) => {
        try {
            const response = await fetch(`${config.API_URL}/documents/${doc.id}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                throw new Error("Erreur lors de la suppression du document");
            }

            setDocuments(prev => {
                const newDocuments = { ...prev };
                delete newDocuments[doc.id];
                return newDocuments;
            });
        } catch (err) {
            setError(err as string);
        } finally {
            setLoading(false);
        }
    }, []);

    const value = {
        documents,
        loading,
        error,
        addDocument,
        deleteDocument
    };

    return (
        <DocumentContext.Provider value={value}>
            {children}
        </DocumentContext.Provider>
    );
}

// Custom hook to use the document context
export function useDocumentContext() {
    const context = useContext(DocumentContext);
    if (context === undefined) {
        throw new Error('useDocumentContext must be used within a DocumentProvider');
    }
    return context;
}