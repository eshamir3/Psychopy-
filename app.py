from flask import Flask, render_template, redirect, url_for
import subprocess
import os
import json
import sys
import datetime
from flask import request
import re

app = Flask(__name__)

# Default PsychoPy path (can be changed at runtime)
PSYCHOPY_PYTHON_PATH = r"C:\Program Files\PsychoPy\python.exe"

# Load experiments from JSON

def load_experiments():
    try:
        with open('experiment_meta_data/experiments.json', 'r') as f:
            data = json.load(f)
            return data['experiments']

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading experiments: {e}")
        return []
    

# Load and categorize experiments
experiments = load_experiments()
raw_categories = list(set(exp['category'] for exp in experiments))
categories = sorted(raw_categories, key=lambda x: (x != "Memory", x))  # Prioritize 'Memory' on top
with open('experiment_meta_data/exp_manual.json') as f:
    manuals = json.load(f)

@app.route('/')
def index():
    return render_template('index.html', experiments=experiments, categories=categories)

@app.route('/run/<experiment_name>')
def run_experiment(experiment_name):
    global PSYCHOPY_PYTHON_PATH

    # 1. Find the experiment dict
    experiment = next(
        (exp for exp in experiments
         if exp['name'].strip().lower() == experiment_name.strip().lower()),
        None
    )
    if not experiment:
        return render_template('error.html',
                               message=f"Experiment '{experiment_name}' not found.")

    # 2. Resolve script path
    relative_path = experiment.get('path')
    if not relative_path:
        return render_template('not_ready.html', exp_name=experiment_name)

    abs_path = os.path.abspath(relative_path)
    if not os.path.exists(abs_path):
        return render_template('error.html',
                               message=f"File not found at: {abs_path}")

    # 3. Pull defaults from your JSON
    content = manuals.get(experiment['name'], {})
    final_params = {}

    

    for pname, desc, default, option in content.get('parameters', []):
        raw = pname.lower().replace(' ', '_')
        field = re.sub(r'[^a-z0-9_]', '', raw)
        val = request.args.get(field)
        if not val:
            val = default
        final_params[field] = val


    # 4. Prepare log file
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(
        "logs",
        f"{experiment_name.replace(' ', '_')}_{timestamp}.log"
    )

    # 5. Build the PsychoPy CLI command
    cmd = [PSYCHOPY_PYTHON_PATH, abs_path]
    for flag, val in final_params.items():
        cmd += [f"--{flag}", str(val)]

    # 6. Launch
    try:
        with open(log_file, 'w') as log_output:
            subprocess.Popen(
                cmd,
                stdout=log_output,
                stderr=subprocess.STDOUT,
                cwd=os.path.dirname(abs_path),
                creationflags=(subprocess.CREATE_NEW_CONSOLE 
                               if sys.platform == 'win32' else 0)
            )
        # Optionally pass params to the running page for confirmation
        return render_template('experiment_running.html',
                               experiment_name=experiment_name,
                               params=final_params)

    except Exception as e:
        return render_template('error.html',
                               message=f"Error launching experiment: {str(e)}")
    
@app.route('/configure/<experiment_name>')
def configure_experiment(experiment_name):
    # find your experiment dict as you already do
    experiment = next(
        (exp for exp in experiments
         if exp['name'].strip().lower() == experiment_name.strip().lower()),
        None
    )
    if not experiment:
        return render_template('error.html',
                               message=f"No experiment named {experiment_name!r}")

    # grab defaults from your JSON
    content = manuals.get(experiment['name'], {})

    return render_template('configure_experiment.html',
                           experiment=experiment,
                           content=content)


@app.route('/manual/<experiment_name>')
def view_manual(experiment_name):
    # Find the base experiment info from your existing list
    experiment = next(
        (exp for exp in experiments
         if exp['name'].strip().lower() == experiment_name.strip().lower()),
        None
    )
    if not experiment:
        return render_template('error.html',
                               message=f"Manual for '{experiment_name}' not found.")

    # Pull the full manual metadata for this experiment
    content = manuals.get(experiment['name'], {})

    # Render, passing both experiment *and* content to the template
    return render_template(
        'manual.html',
        experiment=experiment,
        content=content
    )

@app.route('/learn_more')
def learn_more():
    return render_template('learn_more.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    path = r"C:\Users\Huize\AppData\Local\Programs\PsychoPy\python.exe"
    if os.path.isfile(path):
        PSYCHOPY_PYTHON_PATH = path

    app.run(debug=True)
