import { DHFC_Document } from '../../types';
import { default_document } from '../../utils';
import { v4 as uuidv4 } from 'uuid';
import EditerDoc from '../EditerDoc';
import { useAddDocument } from '../../hooks/documents';


export default function Ajouter() {
    const { addDocument, loading, error} = useAddDocument();

    const onFinish = (doc: DHFC_Document) => {
        doc.id = uuidv4();
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
            <h1>Ajouter un document</h1>
            <EditerDoc doc={default_document()} onFinish={onFinish} />
        </>
    )
}