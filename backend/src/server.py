from typing import Any, Dict
from flask import Flask, json, request, jsonify
from flask_cors import CORS
import argparse

app = Flask(__name__)
CORS(app)

@app.route('/documents', methods=['GET'])
def get_documents():
    """Return all documents as JSON"""        
    log("Fetching documents")
    if fake_api:
        log_json(documents)
        return jsonify(documents)
    else:
        raise NotImplementedError("Real API not implemented yet")

@app.route('/documents', methods=['POST'])
def add_document():
    """Add a new document from JSON data"""
    log("Adding document")
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data: Dict[str, Any] = request.get_json()
    doc_id = data.get('id')
    if fake_api:
        log_json(data)
        documents[doc_id] = data # type: ignore because a document has an id
    else:
        raise NotImplementedError("Real API not implemented yet") 
    
    return jsonify({"id": doc_id, "document": data}), 201

@app.route('/documents/<string:doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    """Delete a document by UUID"""
    log("Deleting document with ID: " + doc_id)
    if doc_id in documents:
        if fake_api:
            deleted_doc = documents.pop(doc_id)
            log_json(deleted_doc)
        else:
            raise NotImplementedError("Real API not implemented yet")
        return jsonify({"message": "Document deleted", "document": deleted_doc})
    else:
        return jsonify({"error": "Document not found"}), 404

### The rest

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
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind the server to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind the server to')
    parser.add_argument('--graph-db', help='Graph DB server in format "address:port"')
    parser.add_argument('--fake-api', default=False, action='store_true', help='Use fake API for testing')
    parser.add_argument('-v', '--verbose', default=False, action='store_true', help='Enable verbose logging')
    args = parser.parse_args()
    
    # Parse the graph DB server address and port
    if args.fake_api and args.graph_db:
        parser.error("--fake_api and --graph-db are mutually exclusive")
    if args.graph_db:
        try:
            global graph_db_address, graph_db_port
            parts = args.graph_db.split(':')
            graph_db_address = ':'.join(parts[:-1])
            graph_db_port = int(parts[-1])
        except ValueError:
            print("Error: Graph DB server must be in format 'address:port'")
            exit(1)
    if args.fake_api:
        global fake_api, documents
        documents = {}
        fake_api = args.fake_api
    global verbose
    verbose = args.verbose

    return args

if __name__ == '__main__':
    args = parse_arguments()
    app.run(debug=True, host=args.host, port=args.port)