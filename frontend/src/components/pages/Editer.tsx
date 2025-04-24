import { DHFC_Document } from '../../types';
import EditerDoc from '../EditerDoc';
import { useAddDocument } from '../../hooks/documents';
import { useLocation } from 'react-router-dom';


export default function Editer() {
    const location = useLocation();
    const doc = location.state!.doc;
    const { addDocument, loading, error} = useAddDocument();

    const onFinish = (doc: DHFC_Document) => {
        console.log("Document ajouté :", doc);
        addDocument(doc);
    }

    if (error) {
        return <div>Error: {error}</div>;
    }
    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <>
            <h1>Éditer un document</h1>
            <EditerDoc doc={doc} onFinish={onFinish} />
        </>
    )
}