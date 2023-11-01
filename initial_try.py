from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Store annotations in memory as a list of dictionaries
annotations = []

categoryTree = {
    "Structure": {
        "Topics": ["Relevant", "Irrelevant", "Obsolete"],
        "Organization": None,
        "Order of Topics": None,
        "Difficulty": None,
        "Workload": None,
    },
    "Evaluation": {
        "Grading Criteria": ["Assignment", "Quiz", "Midsem/Endsem", "Project", "Presentation", "Labs/Tutorial/Worksheet"],
        "Correctness in Evaluation": ["Fairness", "Biasness", "Transparency"],
        "Solutions": ["Timings of Upload", "Correctness", "Explanation"],
        "Quality of Questions": ["Correctness & Soundness", "Difficulty", "Relevance with Lecture"],
    },
    "Course Material": {
        "Lecture Slides": {
            "Quality": ["Understandability", "Clarity", "Organization", "Presentation"],
            "Timings of Upload": None,
            "Relevance": ["Coverage of Topics", "Relation with Lecture"],
        },
        "Labs/Tutorial/Assignment Questions": {
            "Relevance": None,
            "Quality": ["Pace", "Difficulty"],
        },
        "Extra Material": ["Reference Material", "Practice Sets", "Previous Year Question Papers"],
    },
    "Lecture Delivery": {
        "Teaching Assistants (TAs)": {
            "Punctuality": None,
            "Pedagogical Skills": {
                "Effectiveness": None,
                "Granularity of Teaching": ["High", "Medium", "Fine"],
                "Subject Knowledge": None,
                "Personal Skills": ["Traits", "Voice", "Language"],
                "Interactiveness": ["Approachability", "Peer Engagement"],
            },
        },
        "Professor": {
            "Punctuality": None,
            "Pace": None,
            "Topics Covered": None,
            "Pedagogical Skills": {
                "Effectiveness": None,
                "Granularity of Teaching": ["High", "Medium", "Fine"],
                "Subject Knowledge": None,
                "Personal Skills": ["Traits", "Voice", "Language"],
                "Interactiveness": ["Approachability", "Peer Engagement"],
            },
        },
    },
    "General": {
        "Suggestions": {
            "Course Material": None,
            "Evaluation": None,
            "Lecture": None,
            "Structure": None,
        },
        "Everything": None,
        "Nothing": None,
    },
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/annotate', methods=['POST'])
def annotate():
    text = request.form.get('text')
    sentiment = request.form.get('sentiment')
    categories = request.form.getlist('categories[]')

    annotation = {
        'text': text,
        'terms': [{
            'term': term,
            'categories': getCategoryPath(categoryTree, term),
            'sentiment': sentiment,
        } for term in categories]
    }

    annotations.append(annotation)

    # Save the annotations to a JSON file
    with open('annotations.json', 'a') as json_file:
        json.dump(annotation, json_file)
        json_file.write('\n')

    return jsonify({'success': True})

# Function to get the path to a category from the category tree
def getCategoryPath(tree, category):
    path = []
    for key, value in tree.items():
        if category == key:
            path.append(key)
            break
        if isinstance(value, dict):
            subpath = getCategoryPath(value, category)
            if subpath:
                path.append(key)
                path.extend(subpath)
                break
    return path

if __name__ == '__main__':
    app.run(debug=True)
