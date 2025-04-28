import { DHFC_Document } from '../../types';
import { useDocumentContext } from '../DocumentProvider';
import EditerDoc from '../EditerDoc';
import { useLocation, useNavigate } from 'react-router-dom';

export default function Editer() {
    const { addDocument, loading, error } = useDocumentContext();
    const navigate = useNavigate();
    const location = useLocation();
    const doc = location.state!.doc;


    const onFinish = (doc: DHFC_Document) => {
        console.log("Document ajouté :", doc);
        addDocument(doc);
        navigate("/dashboard");
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