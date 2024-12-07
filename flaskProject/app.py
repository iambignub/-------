from flask import Flask, jsonify, render_template
from pymongo import MongoClient

app = Flask(__name__)

# 连接到MongoDB
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["real_estate"]
collection = db["analysis_results"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    data = list(collection.find({}, {'_id': 0}))
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
