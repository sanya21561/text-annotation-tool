from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_path', methods=['POST'])
def save_path():
    data = request.get_json()
    heading = data.get('heading')
    path = data.get('path')

    existing_data = {}
    try:
        with open('data.json', 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        pass

    # Create a new structure with the input text, category, and subcategories
    new_entry = {
        "heading": heading,
        "category": path
    }

    # Append the new entry to the existing data
    existing_data['data'] = existing_data.get('data', [])
    existing_data['data'].append(new_entry)

    # Save the updated data to the JSON file
    with open('data.json', 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)

    return jsonify({'message': 'Data saved successfully'})

if __name__ == '__main__':
    app.run(debug=True)
