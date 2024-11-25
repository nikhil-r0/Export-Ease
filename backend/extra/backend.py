from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for the frontend

@app.route('/submit-form', methods=['POST'])
def submit_form():
    data = request.get_json()  # Parse JSON data from the request
    print("Received Form Data:", data)

    # Process the data or store it in a database
    # Example: Save the data to a file (or replace with database logic)
    with open("form_data.json", "w") as file:
        import json
        json.dump(data, file, indent=4)

    # Send a response back to the client
    return jsonify({"message": "Form data received successfully!"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
