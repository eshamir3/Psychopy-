from psychopy import visual, event, core, gui, data
import random
import csv

# === CONFIGURATION ===
fixation_time = 0.5  # seconds
stim_time = 2  # seconds max per trial
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

# === PARTICIPANT INFO ===
dlg = gui.Dlg(title="Participant Info")
dlg.addField("Participant ID:")
dlg.addField("Session Number:")
ok_data = dlg.show()
if not dlg.OK:
    core.quit()

participant_id = ok_data[0]
session_number = ok_data[1]

# === SETUP ===
win = visual.Window(size=(800, 600), color='black', units='pix')
fixation = visual.TextStim(win, text='+', color='white')
stimulus = visual.TextStim(win, text='', color='white', height=50)
instruction = visual.TextStim(win, text='', color='white', height=30, wrapWidth=700)

clock = core.Clock()
results = []

# === INSTRUCTIONS ===
def show_instructions():
    text = (
        "Welcome to the Emotional Stroop Task.\n\n"
        "You will see words in different colors.\n"
        "Your job is to press the key corresponding to the color of the word, ignoring its meaning:\n\n"
        f"  {keys['red']} = RED\n  {keys['green']} = GREEN\n  {keys['blue']} = BLUE\n  {keys['yellow']} = YELLOW\n\n"
        "Respond as quickly and accurately as possible.\n\nPress any key to begin the PRACTICE round."
    )
    instruction.text = text
    instruction.draw()
    win.flip()
    event.waitKeys()

# === TRIAL FUNCTION ===
def run_trial(word, color, category, is_practice=False):
    fixation.draw()
    win.flip()
    core.wait(fixation_time)

    stimulus.text = word
    stimulus.color = color
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

    if not is_practice:
        results.append({
            'participant_id': participant_id,
            'session_number': session_number,
            'word': word,
            'color': color,
            'category': category,
            'response_key': key,
            'response_color': response_color if key else None,
            'correct': int(correct),
            'rt': round(rt * 1000) if rt else None
        })

# === BLOCKS ===
def run_practice():
    random.shuffle(practice_words)
    for word in practice_words:
        color = random.choice(colors)
        run_trial(word, color, 'practice', is_practice=True)

def run_main():
    all_trials = []
    for category, words in categories.items():
        selected_words = random.sample(words, 5)
        for word in selected_words:
            color = random.choice(colors)
            all_trials.append((word, color, category))
    random.shuffle(all_trials)
    for word, color, category in all_trials:
        run_trial(word, color, category)

# === SAVE DATA ===
def save_data():
    filename = f"stroop_results_{participant_id}_s{session_number}_{data.getDateStr()}.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"Data saved to {filename}")

# === RUN ===
show_instructions()
run_practice()

instruction.text = "Great job! Now the main task will begin.\n\nPress any key to continue."
instruction.draw()
win.flip()
event.waitKeys()

run_main()
save_data()

instruction.text = "Thank you! The task is complete.\nYou may now exit the experiment."
instruction.draw()
win.flip()
event.waitKeys()

win.close()
core.quit()
