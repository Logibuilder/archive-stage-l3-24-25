interface DHFC_DocumentMetadata {
    name: string;
    author: string;
    date: Date | null
}

export interface DHFC_Document {
    id: string;
    metadata: DHFC_DocumentMetadata;
    content: {
        entities: DHFC_Entity[];
    };
}

export interface DHFC_Entity {
    type: string;
    data: any;
}