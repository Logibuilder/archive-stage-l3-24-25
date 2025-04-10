import { createContext, useContext, useState } from "react";
import { DHFC_Document } from "../../types";
import EditerDoc from "../EditerDoc";
import { getDocuments } from "../../utils";

const Context = createContext({
    doc: null as DHFC_Document | null,
    setDoc: (_doc: DHFC_Document | null) => { },
});

function SelectDoc() {
    const [wantedDoc, setWantedDoc] = useState<DHFC_Document | null>(null);
    const { setDoc } = useContext(Context);
    const documents = getDocuments();

    return (
        <div>
            <h2>Sélectionner un document :</h2>
            <select
                onChange={(e) => {
                    const selectedId = e.target.value;
                    if (selectedId) {
                        const document = documents.find(doc => doc.id === selectedId);
                        setWantedDoc(document!);
                    } else {
                        setWantedDoc(null);
                    }
                }}
            >
                <option value="">-- Sélectionner un document --</option>
                {documents.map(doc => (
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

    return <EditerDoc 
        doc={doc!} 
        onFinish={(doc: DHFC_Document) => {
            alert(`Document modifié :
                Nom: ${doc.metadata.name}
                Auteur: ${doc.metadata.author}
                Date: ${doc.metadata.date}
                Entities: ${doc.content.entities.map(entity => entity.type).join(', ')}
            `);
            setDoc(null);
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