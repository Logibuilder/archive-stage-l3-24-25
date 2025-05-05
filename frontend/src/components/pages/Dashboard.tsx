import { useNavigate } from "react-router-dom";
import { DHFC_Document } from "../../types";
import { confirmPopup } from "../../utils";
import { useDocumentContext } from "../DocumentProvider";

export function Dashboard() {
    const navigate = useNavigate();
    const { getDocuments, deleteDocument, loading, error } = useDocumentContext();

    const handleDelete = (doc: DHFC_Document) => () => {
        confirmPopup(
            "Êtes-vous sûr de vouloir supprimer ce document ?",
            () => {
                deleteDocument(doc);
                console.log("Document supprimé :", doc);
            }
        );
    }

    const makeLine = (doc: DHFC_Document) => {
        return (
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <p>{doc.metadata.name} / {doc.metadata.author} / {doc.metadata.date?.toString()}</p>
                <button onClick={() => { navigate("/voir", { state: { doc } }) }}>Voir</button>
                <button onClick={() => { navigate("/editer", { state: { doc } }) }}>Éditer</button>
                <button onClick={handleDelete(doc)}>Supprimer</button>
            </div>
        );
    }

    const documents = getDocuments();

    if (error) {
        return <div>Error: {error}</div>;
    }
    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>Dashboard</h1>
            <button onClick={() => { navigate("/ajouter") }}>Ajouter un document</button>
            <h2>Documents :</h2>
            <div>
                {Object.values(documents).length > 0 
                    ? Object.values(documents).map(doc => makeLine(doc))
                    : <p>Aucun document</p>
                }
            </div>
        </div>
    );
}