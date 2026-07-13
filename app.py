# Flask Backend API for Handwritten Digit Recognition

from flask import Flask, request, jsonify
import numpy as np
from sklearn.datasets import load_digits
from sklearn.ensemble import RandomForestClassifier
import pickle

app = Flask(__name__)

# Load the pre-trained model
try:
    with open('models/trained_model.pkl', 'rb') as f:
        model = pickle.load(f)
except:
    print('Warning: Could not load pre-trained model')
    model = None

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict digit from image data"""
    try:
        data = request.json
        image_data = np.array(data['image']).reshape(1, -1)
        
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        prediction = model.predict(image_data)[0]
        confidence = model.predict_proba(image_data).max()
        
        return jsonify({
            'prediction': int(prediction),
            'confidence': float(confidence)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
