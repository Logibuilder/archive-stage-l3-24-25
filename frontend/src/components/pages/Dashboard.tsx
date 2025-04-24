import { useNavigate } from "react-router-dom";
import { useDeleteDocument, useGetDocuments } from "../../hooks/documents";
import { DHFC_Document } from "../../types";
import { confirmPopup } from "../../utils";

export function Dashboard() {
    const { documents, refreshDocuments, loading: loadingGet, error: errorGet } = useGetDocuments();
    const { deleteDocument, loading: loadingDelete, error: errorDelete } = useDeleteDocument();
    const navigate = useNavigate();

    const handleDelete = (doc: DHFC_Document) => () => {
        confirmPopup(
            "Êtes-vous sûr de vouloir supprimer ce document ?",
            () => {
                deleteDocument(doc);
                console.log("Document supprimé :", doc);
                refreshDocuments();
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

    if (errorGet || errorDelete) {
        return <div>Error: {errorGet?.toString() || errorDelete?.toString()}</div>;
    }
    if (loadingGet || loadingDelete) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>Dashboard</h1>
            <button onClick={() => { navigate("/ajouter") }}>Ajouter un document</button>
            <h2>Documents :</h2>
            <div className="documents-list">
                {Object.values(documents).map(doc => makeLine(doc))}
            </div>
        </div>
    );
}