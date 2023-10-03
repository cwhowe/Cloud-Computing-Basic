from flask import Flask, request, jsonify
import threading
import logging

app = Flask(__name__)

# In-memory data store
data_store = {}
data_lock = threading.Lock()

logging.basicConfig(filename="key_value_store.log", level=logging.INFO, format='%(asctime)s - %(message)s')

@app.route('/get/<key>', methods=['GET'])
def get_value(key):
    with data_lock:
        value = data_store.get(key)
        if value is None:
            logging.info(f"GET operation on key: {key} failed. Key not found.")
            return jsonify({"error": "Key not found"}), 404
        
        logging.info(f"GET operation on key: {key} succeeded.")
        return jsonify({"value": value})

@app.route('/put', methods=['PUT'])
def put_value():
    content = request.json
    key = content["key"]
    value = content["value"]

    with data_lock:
        data_store[key] = value
        
    logging.info(f"PUT operation on key: {key}, value: {value} succeeded.")
    return jsonify({"message": f"Value for {key} set successfully."})

@app.route('/del/<key>', methods=['DELETE'])
def del_value(key):
    with data_lock:
        if key not in data_store:
            logging.info(f"DEL operation on key: {key} failed. Key not found.")
            return jsonify({"error": "Key not found"}), 404
        
        del data_store[key]
        
    logging.info(f"DEL operation on key: {key} succeeded.")
    return jsonify({"message": f"Key {key} deleted successfully."})

@app.route('/', methods=['GET'])
def homepage():
    return "Welcome to the Key-Value Store!"


if __name__ == '__main__':
    app.run(port=8080)
