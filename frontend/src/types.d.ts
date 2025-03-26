interface DocumentMetadata {
    name: string;
    author: string;
    date: Date;
}

interface Document {
    metadata: DocumentMetadata;
    content: {
        entities: Entity[];
    };
}

interface Entity {
    type: string;
    data: any;
}

// Export for usage elsewhere
export { Document };
export { Entity };