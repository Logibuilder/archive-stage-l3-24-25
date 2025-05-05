from typing import Any, Dict
from flask import Flask, json, request, jsonify
from flask_cors import CORS
import argparse
import os

from DHFCTools import mapOntology

app = Flask(__name__)
CORS(app)

domain_ontology = {}

@app.route('/documents', methods=['GET'])
def get_documents():
    """Return all documents as JSON"""        
    log("Fetching documents")
    #documents = getDocuments()
    documents = {}
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
    parse_arguments()
    init_domain_ontology()
    app.run(debug=True, host=config["host"], port=config["port"])