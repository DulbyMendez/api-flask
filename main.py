from flask import Flask, jsonify, request
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

""" load_dotenv(dotenv_path=".env")
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
db = firestore.client() """

@app.route('/')
def index():
    return jsonify({'message': 'Hello Elizabeth and Emily!'})

""" @app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = []
    for doc in db.collection('categories').stream():
        categories.append(doc.to_dict())
    return {"categories":categories}

@app.route('/api/category', methods=['GET', 'POST'])
def create_category():
    data = request.get_json()
    # Validar los datos de la categoría (opcional)
    # ...
    category_ref = db.collection('categories').document()
    category_ref.set(data)
    return jsonify({'message': 'Categoría creada correctamente'}), 200
 """

if __name__ == '__main__':
    app.run(debug=True)