from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.get_json()
    sentence = data.get('sentence')
    texts = data.get('texts')

    # Load the existing JSON data (if any)
    existing_data = {}
    try:
        with open('data.json', 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        pass

    # Create a new structure with the sentence and associated text-path pairs
    new_entry = {
        "sentence": sentence,
        "texts": texts
    }

    # Append the new entry to the existing data
    existing_data['sentences'] = existing_data.get('sentences', [])
    existing_data['sentences'].append(new_entry)

    # Save the updated data to the JSON file
    with open('data.json', 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)

    return jsonify({'message': 'Data saved successfully'})

if __name__ == '__main__':
    app.run(debug=True)
