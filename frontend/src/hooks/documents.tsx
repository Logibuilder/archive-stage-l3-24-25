import { useCallback, useEffect, useState } from "react";
import { DHFC_Document } from "../types";
import config from "../config";
import { fake_data } from "../utils";

export function useGetDocuments() {
    const [documents, setDocuments] = useState<DHFC_Document[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [refresh, setRefresh] = useState(false);

    const refreshDocuments = useCallback(() => {
        setRefresh(prev => !prev);
    }, []);

    useEffect(() => {
        (async () => {
            try {
                if (config.FAKE_DATA) {
                    setDocuments(Object.values(fake_data));
                } else {
                    const response = await fetch(`${config.API_URL}/documents`);
                    if (!response.ok) {
                        throw new Error("Erreur lors de la récupération des documents");
                    }
                    setDocuments(await response.json());
                }
            } catch (err) {
                setError(err as string);
            } finally {
                setLoading(false);
            }
        })();
    }, [refresh]);

    return { documents, refreshDocuments, loading, error };
}

export function useAddDocument() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const addDocument = useCallback(async (document: DHFC_Document) => {
        try {
            if (config.FAKE_DATA) {
                fake_data[document.id] = document;
            } else {
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
            }
        } catch (err) {
            setError(err as string);
        } finally {
            setLoading(false);
        }
    }, []);

    return { addDocument, loading, error };
}

export function useDeleteDocument() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const deleteDocument = useCallback(async (doc: DHFC_Document) => {
        try {
            if (config.FAKE_DATA) {
                delete fake_data[doc.id];
            } else {
                const response = await fetch(`${config.API_URL}/documents/${doc.id}`, {
                    method: 'DELETE',
                });

                if (!response.ok) {
                    throw new Error("Erreur lors de la suppression du document");
                }
            }
        } catch (err) {
            setError(err as string);
        } finally {
            setLoading(false);
        }
    }, []);
    return { deleteDocument, loading, error };
}