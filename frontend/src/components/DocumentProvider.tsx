import { createContext, useCallback, useContext, useState, ReactNode, useEffect } from 'react';
import { DHFC_Document } from '../types';
import config from '../config';

// Create the context with a default value
interface DocumentContextType {
    domain_ontology: Record<string, any>;
    loading: boolean;
    error: string | null;
    getDocuments: () => Promise<Record<string, DHFC_Document>>;
    addDocument: (document: DHFC_Document) => Promise<void>;
    deleteDocument: (document: DHFC_Document) => Promise<void>;
}

const DocumentContext = createContext<DocumentContextType | undefined>(undefined);

export function DocumentProvider({ children }: { children: ReactNode }) {
    const [documents, setDocuments] = useState<Record<string, DHFC_Document>>({});
    const [domain_ontology, setDomainOntology] = useState<Record<string, any>>({});
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [refresh, setRefresh] = useState(false);

    // get domain ontology
    useEffect(() => {
        (async () => {
            try {
                const response = await fetch(`${config.API_URL}/domain_ontology`);
                if (!response.ok) {
                    throw new Error("Erreur lors de la récupération de l'ontologie de domaine");
                }
                setDomainOntology(await response.json());
            } catch (err) {
                setError(err instanceof Error ? err.message : String(err));
            } finally {
                setLoading(false);
            }
        })();
    }, []);

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
                setError(err instanceof Error ? err.message : String(err));
            } finally {
                setLoading(false);
            }
        })();
    }, [refresh]);

    const refreshDocuments = () => {
        setRefresh(prev => !prev);
    }

    const getDocuments = useCallback(async () => {
        refreshDocuments();
        return documents;
    }, [documents]);

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

            refreshDocuments();
        } catch (err) {
            setError(err instanceof Error ? err.message : String(err));
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

            refreshDocuments();
        } catch (err) {
            setError(err instanceof Error ? err.message : String(err));
        } finally {
            setLoading(false);
        }
    }, []);

    const value = {
        domain_ontology,
        loading,
        error,
        getDocuments,
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