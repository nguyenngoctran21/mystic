from flask import Flask, request, jsonify
from tool import run

app = Flask(__name__)

@app.route('/')
def home():
    return {"status": "Mystic API running"}

@app.route('/api/profile', methods=['POST'])
def profile():
    try:
        data = request.get_json()
        result = run(data)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run()
