import { DHFC_Document } from "./types";
import { v4 as uuidv4 } from 'uuid';

export function placeholder_entity(doc_num: number, num: number) {
    return {
        type: `Entity ${doc_num}-${num}`,
        data: `Data ${doc_num}-${num}`
    };
}

export function placeholder_document(num: number): DHFC_Document {
    return {
        id: uuidv4(),
        metadata: {
            name: `Document ${num}`,
            author: `Author ${num}`,
            date: new Date()
        },
        content: {
            entities: [
                placeholder_entity(num, 1),
                placeholder_entity(num, 2),
            ]
        }
    };
}

export function default_document() {
    return {
        id: uuidv4(),
        metadata: {
            name: '',
            author: '',
            date: null
        },
        content: {
            entities: []
        }
    };
}

export function default_entity() {
    return {
        type: '',
        data: null
    };
}

export function print_doc(doc: DHFC_Document) {
    const metadata = (
        <div>
            <p>Name: {doc.metadata.name}</p>
            <p>Author: {doc.metadata.author}</p>
            <p>Date: {doc.metadata.date?.toString()}</p>
        </div>
    )

    const entities = doc.content.entities.map((entity, index) => print_entity(entity, index));

    return (
        <div>
            {metadata}
            <h2>Entities:</h2>
            <div className="entities-list">
                {entities}
            </div>
        </div>
    );
}

export function print_entity(entity: any, index: number) {
    return (
        <div key={index}>
            <p>Type: {entity.type}</p>
            <p>Data: {entity.data}</p>
        </div>
    );
}

export function confirmPopup(
    message: string = "Êtes-vous sûr de vouloir continuer ?",
    actionCallback: () => void,
): void {
    const isConfirmed = window.confirm(message);

    if (isConfirmed) {
        actionCallback();
    }
}
