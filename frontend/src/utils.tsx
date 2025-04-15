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

export const fake_data = (() => {
    const doc1 = placeholder_document(1);
    const doc2 = placeholder_document(2);
    return {
        [doc1.id]: doc1,
        [doc2.id]: doc2,
    };
})();