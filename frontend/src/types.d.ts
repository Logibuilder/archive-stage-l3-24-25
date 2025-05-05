interface DHFC_DocumentMetadata {
    name: string;
    author: string;
    date: Date | null;
}

export interface DHFC_Document {
    id: string;
    metadata: DHFC_DocumentMetadata;
    entities: DHFC_Entity[];
}

export interface DHFC_Entity {
    name: string;
    type_uri: string;
    assertions: DHFC_Assertion[];
}

export interface DHFC_Assertion {
    property_uri: string;
    object_name: string;
}

export interface DHFC_Property {
    property_uri: string;
    temporality: boolean;
    range: string;
    type: string;
    time?: string;
    label?: string;
    inverse_uri?: string;
}