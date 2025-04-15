import { createContext, useContext, useState } from "react";
import { DHFC_Document } from "../../types";
import EditerDoc from "../EditerDoc";
import { useAddDocument, useGetDocuments } from "../../hooks/documents";

const Context = createContext({
    doc: null as DHFC_Document | null,
    setDoc: (_doc: DHFC_Document | null) => { },
});

function SelectDoc() {
    const [wantedDoc, setWantedDoc] = useState<DHFC_Document | null>(null);
    const { setDoc } = useContext(Context);
    const { documents, loading, error } = useGetDocuments();

    if (error) {
        return <div>Error: {error}</div>;
    }
    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h2>Sélectionner un document :</h2>
            <select
                onChange={(e) => {
                    const selectedId = e.target.value;
                    if (selectedId) {
                        const document = documents[selectedId];
                        setWantedDoc(document!);
                    } else {
                        setWantedDoc(null);
                    }
                }}
            >
                <option value="">-- Sélectionner un document --</option>
                {Object.values(documents).map(doc => (
                    <option key={doc.id} value={doc.id}>
                        {doc.metadata.name} : {doc.metadata.author}
                    </option>
                ))}
            </select>
            <button
                disabled={!wantedDoc}
                onClick={() => {
                    setDoc(wantedDoc);
                }}
            >
                Éditer
            </button>
        </div>
    );
}

function EditDoc() {
    const { doc, setDoc } = useContext(Context);
    const { addDocument, loading, error } = useAddDocument();
    if (error) {
        return <div>Error: {error}</div>;
    }
    if (loading) {
        return <div>Loading...</div>;
    }

    return <EditerDoc
        doc={doc!}
        onFinish={(doc: DHFC_Document) => {
            addDocument(doc);
            setDoc(null);
            console.log("Document modifié :", doc);
        }}
    />;
}

export default function Editer(): React.ReactElement {
    const [doc, setDoc] = useState<DHFC_Document | null>(null);

    return (
        <>
            <h1>Éditer un document</h1>
            <Context.Provider value={{ doc, setDoc }}>
                {doc ? <EditDoc /> : <SelectDoc />}
            </Context.Provider>
        </>
    );
}