from flask import Flask, jsonify, request
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

load_dotenv(dotenv_path=".env")
credentials_env = {
    "type": 'service_account',
    "project_id": os.environ.get('PROJECT_ID'),
    "private_key_id": os.environ.get('PRIVATE_KEY_ID'),
    "private_key": os.environ.get('PRIVATE_KEY'),
    "client_email": os.environ.get('CLIENT_EMAIL'),
    "client_id": os.environ.get('CLIENT_ID'),
    "auth_uri": os.environ.get('AUTH_URI'),
    "token_uri": os.environ.get('TOKEN_URI'),
    "auth_provider_x509_cert_url": os.environ.get('AUTH_PROVIDER_X509_CERT_URL'),
    "client_x509_cert_url": os.environ.get('CLIENT_X509_CERT_URL'),
    "universe_domain": os.environ.get('UNIVERSE_DOMAIN'),
}
cred = credentials.Certificate(credentials_env)
firebase_admin.initialize_app(cred)
db = firestore.client()

error_message = {
            "status": "error",
            "message": "Ha ocurrido un error inesperado"
    }

@app.route('/')
def index():
    return jsonify({
        "status": "success",
        'message': 'Welcome to my DB'
    })

@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = []
    for doc in db.collection('categories').stream():
        document_id = doc.id  # Get the document ID
        document_data = doc.to_dict()  # Get the document data (including ID)
        combined_data = {
            "id": document_id,  # Add the ID to the data
            **document_data  # Unpack the existing document data
        }
        categories.append(combined_data)
        """ categories.append(doc.to_dict()) """
    if (categories):
        return jsonify({
            "status": "success",
            "message": "Categories querried successfully",
            "data":categories
        })
    else : return jsonify(error_message)

@app.route('/api/categories/<id>', methods=['GET'])
def get_category_id(id):
    doc_ref = db.collection('categories').document(id)
    doc = doc_ref.get()

    if doc.exists:
        data = doc.to_dict()
        return jsonify({
            "status": "success",
            "message": "Category successfully querried",
            "data": data
        })
    else:
        return jsonify({'message': 'Document not found'}), 404

@app.route('/api/category', methods=['POST'])
def create_category():
    data = request.get_json()
    # Validar los datos de la categoría (opcional)
    category_ref = db.collection('categories').document()
    category_ref.set(data)
    if (category_ref):
        return jsonify({
            "status": "success",
            "message": "Categoría creada correctamente",
            "data":category_ref
        }), 200
    else: jsonify(error_message)

@app.route('/api/category-seed', methods=['POST'])
def seed_categories():
    categories_data = [
        {"name": "Lectura", "description": "Libros, revistas, artículos", "created_at": "10-08-1985"},
        {"name": "Ejercicio", "description": "Deportes, entrenamiento, fitness", "created_at": "10-08-1985"},
        {"name": "Películas y Series", "description": "Cine, televisión, streaming", "created_at": "10-08-1985"},
        {"name": "Videojuegos", "description": "Consolas, juegos de PC, juegos móviles", "created_at": "10-08-1985"},
        {"name": "Recetas y Cocina", "description": "Recetas, cocina, gastronomía", "created_at": "10-08-1985"},
        {"name": "Música", "description": "Escuchar música, tocar instrumentos, conciertos", "created_at": "10-08-1985"},
        {"name": "Otros", "description": "Cualquier otra actividad", "created_at": "10-08-1985"},
    ]
    try:
        all_categories_data = []
        for category in categories_data:
            category_ref = db.collection('categories').document()
            category_ref.set(category)
            category_data = category_ref.get().to_dict()
            all_categories_data.append(category_data)
        return jsonify({
            "status": "success",
            "message": "Categoría creada correctamente",
            "data":all_categories_data
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al sembrar las categorías: {str(e)}"
        }), 500
        """ jsonify(error_message) """


if __name__ == '__main__':
    app.run(debug=True)