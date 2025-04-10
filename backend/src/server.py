from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# In-memory document storage (would use a database in production)
documents = {}

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
    doc_id = str(uuid.uuid4())  # Generate a unique ID
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)