from flask import Flask, request, jsonify
import uuid
import argparse

app = Flask(__name__)

documents = {}
# these are never empty, because required in the command line arguments
graph_db_address: str = ""
graph_db_port: int = 0

@app.route('/documents', methods=['GET'])
def get_documents():
    """Return all documents as JSON"""
    return jsonify(documents)

@app.route('/documents', methods=['POST'])
def add_document():
    """Add a new document from JSON data"""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    doc_id = str(uuid.uuid4())  # Change
    documents[doc_id] = data
    
    return jsonify({"id": doc_id, "document": data}), 201

@app.route('/documents/<string:doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    """Delete a document by UUID"""
    if doc_id in documents:
        deleted_doc = documents.pop(doc_id)
        return jsonify({"message": "Document deleted", "document": deleted_doc})
    else:
        return jsonify({"error": "Document not found"}), 404

### The rest

def parse_arguments():
    """Parse command line arguments for Flask server"""
    parser = argparse.ArgumentParser(description='Run the document API server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind the server to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind the server to')
    parser.add_argument('--graph-db', required=True, help='Graph DB server in format "address:port"')
    args = parser.parse_args()
    
    # Parse the graph DB server address and port
    global graph_db_address, graph_db_port
    try:
        parts = args.graph_db.split(':')
        graph_db_address = ':'.join(parts[:-1])
        graph_db_port = int(parts[-1])
    except ValueError:
        print("Error: Graph DB server must be in format 'address:port'")
        exit(1)

    return args

if __name__ == '__main__':
    args = parse_arguments()
    app.run(debug=True, host=args.host, port=args.port)