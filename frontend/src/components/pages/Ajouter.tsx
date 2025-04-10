import { DHFC_Document } from '../../types';
import { default_document } from '../../utils';
import EditerDoc from '../EditerDoc';

const onFinish = (doc: DHFC_Document) => {
    alert(`Document ajouté : 
        Nom: ${doc.metadata.name}
        Auteur: ${doc.metadata.author}
        Date: ${doc.metadata.date}
        Entities: ${doc.content.entities.map(entity => entity.type).join(', ')}
    `);
}

export default function Ajouter() {
    return (
        <>
            <h1>Ajouter un document</h1>
            <EditerDoc doc={default_document()} onFinish={onFinish} />
        </>
    )
}