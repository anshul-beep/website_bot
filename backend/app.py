from flask import Flask,jsonify
from api.routes import api_bp

app = Flask(__name__)

app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Flask app is running. Use /api/store-embeddings to store vector embeddings."}), 200

if __name__ == "__main__":
    app.run(debug=True)
