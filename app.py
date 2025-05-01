from flask import Flask, render_template, redirect, url_for
import subprocess
import os

app = Flask(__name__)

# Define experiments
experiments = [
    {'name': 'SART Task', 'description': 'Measure sustained attention and inhibition.', 'category': 'Attention'},
    {'name': 'Rapid Attention', 'description': 'Test quick attention switching.', 'category': 'Attention'},
    {'name': 'Focused Blink', 'description': 'Visual focus reaction time.', 'category': 'Attention'},
    {'name': 'Memory Recall', 'description': 'Short-term memory accuracy test.', 'category': 'Memory'},
    {'name': 'Working Memory', 'description': 'Span and recall capacity test.', 'category': 'Memory'},
    {'name': 'Long-Term Memory', 'description': 'Delayed recall after distraction.', 'category': 'Memory'},
    {'name': 'Consonant Trigram Task (Peterson & Peterson, 1959)', 'description': 'Recall the trigram from memory', 'category': 'Memory'},
    {'name': 'Emotional Stroop', 'description': 'Emotion-word interference task.', 'category': 'Cognitive Control'},
    {'name': 'Task Switching', 'description': 'Shift attention between tasks.', 'category': 'Cognitive Control'},
    {'name': 'Executive Conflict', 'description': 'Manage conflicting cognitive demands.', 'category': 'Cognitive Control'},
    {'name': 'Reaction Speed', 'description': 'Measure simple reaction time.', 'category': 'Processing Speed'},
    {'name': 'Visual Search', 'description': 'Find targets among distractors.', 'category': 'Processing Speed'},
    {'name': 'Motor Response', 'description': 'Record motor reaction times.', 'category': 'Processing Speed'},
    {'name': 'Decision Risk', 'description': 'Make decisions under uncertainty.', 'category': 'Decision Making'},
    {'name': 'Value Choice', 'description': 'Choose between rewards.', 'category': 'Decision Making'},
    {'name': 'Strategy Shift', 'description': 'Adapt to changing environments.', 'category': 'Decision Making'},
]

# Categories
categories = ["Attention", "Memory", "Cognitive Control", "Processing Speed", "Decision Making"]

# Adjust your path to PsychoPy python if needed
PSYCHOPY_PYTHON_PATH = r"C:\Program Files\PsychoPy\python.exe"
SART_SCRIPT_PATH = os.path.join("SART", "SART_EXP.py")

@app.route('/')
def index():
    return render_template('index.html', experiments=experiments, categories=categories)

@app.route('/run/<experiment_name>')
def run_experiment(experiment_name):
    if experiment_name == "SART Task":
        # Launch the PsychoPy experiment!
        subprocess.Popen([PSYCHOPY_PYTHON_PATH, SART_SCRIPT_PATH])
        return render_template('experiment_running.html', experiment_name=experiment_name)
    elif experiment_name == 'Consonant Trigram Task (Peterson & Peterson, 1959)':
        # Launch the PsychoPy experiment!
        script_path = os.path.join("TRIGRAM", "TRIGRAM_EXP.py")
        subprocess.Popen([PSYCHOPY_PYTHON_PATH, script_path])
        return render_template('experiment_running.html', experiment_name=experiment_name)
    else:
        return f"<h1>Experiment '{experiment_name}' is not ready yet. 🚧</h1><br><a href='/'>Return Home</a>"

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
