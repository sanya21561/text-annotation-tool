from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_path', methods=['POST'])
def save_path():
    data = request.get_json()
    path = data.get('path')

    # Load the existing JSON data (if any)
    existing_data = {}
    try:
        with open('paths.json', 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        pass

    # Append the new path to the existing data
    existing_data['paths'] = existing_data.get('paths', [])
    existing_data['paths'].append(path)

    # Save the updated data to the JSON file
    with open('paths.json', 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)

    return jsonify({'message': 'Path saved successfully'})

if __name__ == '__main__':
    app.run(debug=True)
