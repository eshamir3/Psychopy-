from psychopy import visual, event, core, gui, data
import random
import csv
import os

# === FIXED CONFIG ===
keys = {'red': 'd', 'green': 'f', 'blue': 'j', 'yellow': 'k'}
colors = ['red', 'green', 'blue', 'yellow']
categories = {
    'neutral': ["table", "window", "book", "chair", "pencil", "clock", "paper"],
    'aggression': ["punch", "hit", "rage", "fight", "stab", "abuse", "kill"],
    'positive': ["love", "joy", "smile", "peace", "kind", "happy", "hug"],
    'negative': ["sad", "grief", "pain", "angry", "lonely", "upset", "fear"],
    'color': ["purple", "orange", "white", "brown", "pink", "gray", "black"]
}
practice_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]

# === GUI CONFIGURATION ===
# --- 1. Participant Info ---
expInfo = {
    'Participant ID': '',
    'Session': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],  # Dropdown menu
    'Show Instructions': True,  # Toggle for instructions
    'Practice Trials': True,    # Toggle for practice
    'Number of Practice Trials': 10,  # How many practice trials
    'Number of Main Trials': 100,     # How many main trials
    'Stimulus Duration (sec)': 0.5,   # How long each word shows
    'Response Window (sec)': 2.0,     # Time allowed to respond
    'ITI Duration (sec)': 0.5         # Time between trials
}

dlg = gui.DlgFromDict(expInfo, title="Emotional Stroop Task", 
                     order=['Participant ID', 'Session', 'Show Instructions', 'Practice Trials', 
                           'Number of Practice Trials', 'Number of Main Trials', 
                           'Stimulus Duration (sec)', 'Response Window (sec)', 'ITI Duration (sec)'])
if not dlg.OK:
    core.quit()

# === EXTRACT CONFIGURATION ===
participant_id = expInfo['Participant ID']
session_number = expInfo['Session']
stim_time = float(expInfo['Stimulus Duration (sec)'])
fixation_time = float(expInfo['Response Window (sec)'])

selected_categories = {}
if expInfo['neutral']: selected_categories['neutral'] = categories['neutral']
if expInfo['aggression']: selected_categories['aggression'] = categories['aggression']
if expInfo['positive']: selected_categories['positive'] = categories['positive']
if expInfo['negative']: selected_categories['negative'] = categories['negative']
if expInfo['color']: selected_categories['color'] = categories['color']

# === SETUP WINDOW AND STIMULI ===
win = visual.Window(size=(1024, 768), color="white", units="pix", fullscr=False)
instruction_text = visual.TextStim(win, text='', color='black', wrapWidth=800)
stimulus_text = visual.TextStim(win, text='', color='black', height=0.2)
feedback_text = visual.TextStim(win, text='', color='green', wrapWidth=800)
fixation = visual.TextStim(win, text='+', color='black', height=0.1)
continue_text = visual.TextStim(win, text='Press SPACE to continue', color='black', pos=(0, -300))

clock = core.Clock()
results = []

# === INSTRUCTIONS ===
def show_instructions():
    heading = visual.TextStim(win, text="Instructions", color='white', height=60, pos=(0, 250))
    heading.draw()
    win.flip()
    core.wait(1.5)

    instruction_text.text = (
        "Welcome to the Color Word Game!\n\n"
        "Here's how to play:\n"
        "• Words will appear in different colors\n"
        "• Press the key that matches the COLOR of the word:\n"
        "  RED = R key\n"
        "  BLUE = B key\n"
        "  GREEN = G key\n"
        "  YELLOW = Y key\n\n"
        "Ignore what the word says, just focus on its color!"
    )
    instruction_text.height = 30
    instruction_text.pos = (0, 100)
    instruction_text.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

    # Image examples (use your own images)
    example_images = ['example1.png', 'example2.png']
    for img_file in example_images:
        image = visual.ImageStim(win, image=img_file, size=(600, 400))
        image.draw()
        win.flip()
        event.waitKeys()

    instruction_text.text = (
        "Great!\n\n"
        "- Look at the COLOR\n"
        "- Press the matching key\n"
        "- Try to be quick and right!\n\n"
        "Press any key to start practice."
    )
    instruction_text.pos = (0, 0)
    instruction_text.draw()
    win.flip()
    event.waitKeys()

# === TRIAL FUNCTION ===
def run_trial(word, color, category, is_practice=False):
    fixation.draw()
    win.flip()
    core.wait(fixation_time)

    stimulus_text.text = word
    stimulus_text.color = color
    win.flip()

    clock.reset()
    keys_pressed = event.waitKeys(maxWait=stim_time, keyList=list(keys.values()), timeStamped=clock)

    win.flip()
    core.wait(0.25)

    if keys_pressed:
        key, rt = keys_pressed[0]
        response_color = [k for k, v in keys.items() if v == key][0]
        correct = (response_color == color)
    else:
        key, rt = None, None
        correct = False
        response_color = None

    if not is_practice:
        results.append({
            'participant_id': participant_id,
            'session_number': session_number,
            'word': word,
            'color': color,
            'category': category,
            'response_key': key,
            'response_color': response_color,
            'correct': int(correct),
            'rt': round(rt * 1000) if rt else None
        })

# === PRACTICE ===
def run_practice():
    random.shuffle(practice_words)
    for word in practice_words:
        color = random.choice(colors)
        run_trial(word, color, 'practice', is_practice=True)

# === MAIN EXPERIMENT ===
def run_main():
    all_trials = []
    for category, words in selected_categories.items():
        selected_words = random.sample(words, 5)
        for word in selected_words:
            color = random.choice(colors)
            all_trials.append((word, color, category))
    random.shuffle(all_trials)
    for word, color, category in all_trials:
        run_trial(word, color, category)

# === SAVE DATA ===
def save_data(duration):
    filename = f"stroop_results_{participant_id}_s{session_number}_{data.getDateStr()}.csv"
    with open(filename, mode='w', newline='') as file:
        fieldnames = list(results[0].keys()) + ['experiment_duration']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            row['experiment_duration'] = duration
            writer.writerow(row)
    print(f"Data saved to {filename}")

# === RUN FULL TASK ===
show_instructions()
run_practice()

instruction_text.text = "Great job! Now the main task will begin.\n\nPress any key to continue."
instruction_text.draw()
win.flip()
event.waitKeys()

start_time = core.getTime()
run_main()
end_time = core.getTime()
duration = round(end_time - start_time, 2)

save_data(duration)

instruction_text.text = f"Thank you! You're done!\nTotal Time: {duration} seconds.\nPress any key to close."
instruction_text.draw()
win.flip()
event.waitKeys()

win.close()
core.quit()
