from typing import Any, Dict
from flask import Flask, json, request, jsonify
from flask_cors import CORS
import argparse
import os

from DHFCTools import mapOntology
from DHFCMonoBuildTools import newAssertionSet
from DHFCTools import generate

app = Flask(__name__)
CORS(app)

domain_ontology = {}


def addDocument(document):

    #convert json data to dictionary
    #doc = document

    data = transform(document)

    assertions = generate(data[0], data[1] )

    newAssertionSet(document["metadata"]["name"], document1["metadata"]["author"], assertions)
    print("document added succesfully")




def transform(document) :

    entity_dic = {}
    for entity in document["entities"]:

        entity_name = entity["name"]

        entity_type_uri = entity["type_uri"]
        print("l'entity_name est : " + entity_name)
        print("l'entity_type_uri est : " +  entity_type_uri)

        assertions = []
        for assertion in entity["assertions"]:
            doc_type_url = assertion["property"]

            property = property_uri_to_dic(doc_type_url , entity_type_uri)

            doc_object_name = assertion["object_name"]

            assertion = (
                doc_type_url,
                property,
                doc_object_name
            )

            assertions.append(assertion)

        assertions_class[entity_name] = {
            "class" : entity_type_uri,
            "assertions" : assertions
        }


    tuple = ( assertions_class  , entity_type_uri)
    return tuple

@app.route('/documents', methods=['GET'])
def get_documents():
    """Return all documents as JSON"""        
    log("Fetching documents")
    documents = getDocuments()
    log_json(documents)
    return jsonify(documents)

@app.route('/documents', methods=['POST'])
def add_document():
    """Add a new document from JSON data"""
    log("Adding document")
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data: Dict[str, Any] = request.get_json()
    log_json(data)
    addDocument(data)
    raise NotImplementedError("Real API not implemented yet") 
    
    return jsonify({"message": "Document added"})

@app.route('/documents/<string:doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    """Delete a document by UUID"""
    log("Deleting document with ID: " + doc_id)
    try:
        deleteDocument(doc_id)
    except RuntimeError as e:
        return jsonify({"error": e}), 404
    return jsonify({"message": "Document deleted"})

@app.route('/domain_ontology', methods=['GET'])
def get_ontology():
    """Return the domain ontology as JSON"""
    log("Fetching domain ontology")
    log_json(domain_ontology)
    return jsonify(domain_ontology)
    
### Le reste

def property_uri_to_dic(property_uri: str, type_uri: str) -> Dict[str, str]:
    """Convert a property URI to a dictionary with 'property' and 'type' keys"""
    properties = domain_ontology[type_uri]
    for prop in properties:
        if prop["property"] == property_uri:
            return prop
    raise ValueError(f"Property {property_uri} not found in type {type_uri}")

def log(message: str):
    """Log a message if verbose mode is enabled"""
    if verbose:
        print("[LOG]", message)

def log_json(data: Dict[str, Any]):
    """Log JSON data if verbose mode is enabled"""
    if verbose:
        print("[LOG]", json.dumps(data, indent=4))

def parse_arguments():
    """Parse command line arguments for Flask server"""
    parser = argparse.ArgumentParser(description='Run the document API server')
    parser.add_argument('-v', '--verbose', default=False, action='store_true', help='Enable verbose logging')
    args = parser.parse_args()

    global verbose
    verbose = args.verbose
    
    global config
    with open(os.path.join(os.path.dirname(__file__), '../config.json'), 'r') as f:
        config = json.load(f)

# TODO : use this
def init_domain_ontology():
    global domain_ontology
    domain_ontology = mapOntology(config["db"]["query_endpoint"])

if __name__ == '__main__':
    document = {


        "id" : 1,
        "metadata" : {
            "name" : "name1",
            "author" : "auteur",
            "date" : "auj",
        },

        "entities" : [{
            "name" : "name1",
            "type_uri" : "https://naszareck.fr/ontology#Person",
            "assertions" : [
                {
                    "property" : "https://naszareck.fr/ontology#possesses",
                    "object_name" : "name1",
                },
                ]
        }]
    }

    document1 = {
        "id": 1,
        "metadata": {
            "name": "name1",
            "author": "auteur",
            "date": "auj"
        },
        "entities": [
            {
                "name": "name1",
                "type_uri": "https://naszareck.fr/ontology#Person",
                "assertions": [
                    {
                        "property": "https://naszareck.fr/ontology#possesses",
                        "object_name": "name1"
                    }
                ]
            }
        ]
    }

    parse_arguments()
    init_domain_ontology()
    print(json.dumps(domain_ontology, indent=4))
    addDocument(document1)
    app.run(debug=True, host=config["host"], port=config["port"])