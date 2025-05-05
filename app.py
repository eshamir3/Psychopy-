from flask import Flask, render_template, redirect, url_for
import subprocess
import os
import json

app = Flask(__name__)

# Load experiments from JSON file
def load_experiments():
    try:
        with open('experiments.json', 'r') as f:
            data = json.load(f)
            return data['experiments']
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading experiments: {e}")
        return []

# Load experiments
experiments = load_experiments()

# Categories (extracted from experiments)
categories = list(set(exp['category'] for exp in experiments))

# Adjust your path to PsychoPy python if needed
PSYCHOPY_PYTHON_PATH = r"C:\Program Files\PsychoPy\python.exe"

@app.route('/')
def index():
    return render_template('index.html', experiments=experiments, categories=categories)

@app.route('/run/<experiment_name>')
def run_experiment(experiment_name):
    # Find the experiment in our list
    experiment = next((exp for exp in experiments if exp['name'] == experiment_name), None)
    
    if not experiment:
        return f"<h1>Experiment '{experiment_name}' not found. 🚧</h1><br><a href='/'>Return Home</a>"
    
    if not experiment['path']:
        return f"<h1>Experiment '{experiment_name}' is not ready yet. 🚧</h1><br><a href='/'>Return Home</a>"
    
    # Check if the path exists
    if not os.path.exists(experiment['path']):
        return f"<h1>Error: Experiment file not found at {experiment['path']} 🚧</h1><br><a href='/'>Return Home</a>"
    
    try:
        # Launch the PsychoPy experiment
        subprocess.Popen([PSYCHOPY_PYTHON_PATH, experiment['path']])
        return render_template('experiment_running.html', experiment_name=experiment_name)
    except Exception as e:
        return f"<h1>Error launching experiment: {str(e)} 🚧</h1><br><a href='/'>Return Home</a>"

@app.route('/learn_more')
def learn_more():
    return "<h1>Learn More</h1><p>This platform hosts cognitive and behavioral tasks for academic research and internal study use. Carefully structured tasks measure attention, memory, decision making, and processing speed with precision and reliability.</p><br><a href='/'>Return Home</a>"

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    x = input("are you the amazing Huize: (y/n)")
    if x.lower() == 'y':
        PSYCHOPY_PYTHON_PATH = r"C:\Users\Huize\AppData\Local\Programs\PsychoPy\python.exe"
    app.run(debug=True)
