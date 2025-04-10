import { DHFC_Document } from "./types";

export function placeholder_entity(doc_num: number, num: number) {
    return {
        type: `Entity ${doc_num}-${num}`,
        data: `Data ${doc_num}-${num}`
    };
}

export function placeholder_document(num: number): DHFC_Document {
    return {
        id: `${num}`,
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

export function getDocuments(): DHFC_Document[] {
    // TODO: get documents for user from the server
    // for now, sample data
    return [placeholder_document(2), placeholder_document(1)];
}

function placeholder_id() {
    return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
}

export function default_document() {
    return {
        id: placeholder_id(),
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