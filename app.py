from flask import Flask, render_template, redirect, url_for
import subprocess
import os
import json

app = Flask(__name__)

# Default PsychoPy path (can be changed at runtime)
PSYCHOPY_PYTHON_PATH = r"C:\Program Files\PsychoPy\python.exe"

# Load experiments from JSON
def load_experiments():
    try:
        with open('experiments.json', 'r') as f:
            data = json.load(f)
            return data['experiments']
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading experiments: {e}")
        return []

# Load and categorize experiments
experiments = load_experiments()
raw_categories = list(set(exp['category'] for exp in experiments))
categories = sorted(raw_categories, key=lambda x: (x != "Memory", x))  # Prioritize 'Memory' on top

@app.route('/')
def index():
    return render_template('index.html', experiments=experiments, categories=categories)

@app.route('/run/<experiment_name>')
def run_experiment(experiment_name):
    experiment = next(
        (exp for exp in experiments if exp['name'].strip().lower() == experiment_name.strip().lower()),
        None
    )

    if not experiment:
        return f"<h1>Experiment '{experiment_name}' not found. 🚧</h1><br><a href='/'>Return Home</a>"

    path = experiment.get('path')
    if not path:
        return f"<h1>Experiment '{experiment_name}' is not ready yet. 🚧</h1><br><a href='/'>Return Home</a>"

    if not os.path.exists(path):
        return f"<h1>Error: File not found at <code>{path}</code> 🚧</h1><br><a href='/'>Return Home</a>"

    try:
        subprocess.Popen([PSYCHOPY_PYTHON_PATH, path])
        return render_template('experiment_running.html', experiment_name=experiment_name)
    except Exception as e:
        return f"<h1>Error launching experiment: {str(e)} 🚧</h1><br><a href='/'>Return Home</a>"

@app.route('/learn_more')
def learn_more():
    return """
    <h1>Learn More</h1>
    <p>This platform hosts cognitive and behavioral tasks for academic research and internal study use.
    Carefully structured tasks measure attention, memory, decision making, and processing speed
    with precision and reliability.</p>
    <br><a href='/'>Return Home</a>
    """

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    x = input("Are you the H? (y/n): ")
    if x.lower() == 'y':
        PSYCHOPY_PYTHON_PATH = r"C:\Users\Huize\AppData\Local\Programs\PsychoPy\python.exe"
    app.run(debug=True)
