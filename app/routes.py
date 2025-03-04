from flask import Blueprint, render_template, jsonify, request
from agents.crypto_data_agent import CryptoDataAgent

main = Blueprint('main', __name__)
crypto_agent = CryptoDataAgent()

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/crypto/advice', methods=['POST'])
def get_crypto_advice():
    data = request.get_json()
    advice = crypto_agent.get_advice(data.get('query', ''))
    return jsonify(advice)
