from typing import Dict

from backend.src.server import domain_ontology

document = {
    "entities": [
        {
            "name": "Albert Einstein",
            "type_uri": "https://naszareck.fr/ontology#hasNumberOfRegenerations",
            "assertions": [
                {
                    "property_url": "https://naszareck.fr/ontology#hasNumberOfRegenerations",
                    "object_name": "German"
                },
                {
                    "property_url": "https://naszareck.fr/ontology#hasNumberOfRegenerations",
                    "object_name": "Physicist"
                }
            ]
        },
        {
            "name": "Theory of Relativity",
            "type_uri": "https://naszareck.fr/ontology#hasNumberOfRegenerations",
            "assertions": [
                {
                    "property_url": "https://naszareck.fr/ontology#hasNumberOfRegenerations",
                    "object_name": "Albert Einstein"
                }
            ]
        }
    ]
}
def property_uri_to_dic(property_uri: str, type_uri: str) -> Dict[str, str]:
    """Convert a property URI to a dictionary with 'property' and 'type' keys"""
    properties = domain_ontology[type_uri]
    for prop in properties:
        if prop["property"] == property_uri:
            return prop
    raise ValueError(f"Property {property_uri} not found in type {type_uri}")

def transform(document) :

    for entity in document.entities:

        entity_name = entity["name"]

        entity_type_uri = entity["type_uri"]

        assertions = []
        for assertion in entity["assertions"]:
            doc_type_url = entity["assertions"]["property_url"]

            property_url = property_uri_to_dic(doc_type_url , entity_type_uri)

            doc_object_name = entity["assertions"]["object_name"]


            assertion [
                "type_url" : property_url,
                "object_name" : doc_object_name,
            ]

            assertions.append(assertion)

        tuple = ( entity_type_uri, assertions )
        print(tuple)