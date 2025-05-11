from psychopy import visual, event, core, gui, data
import random
import csv

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
dlg = gui.Dlg(title="Stroop Task Settings")
dlg.addField("Participant ID:")
dlg.addField("Session Number:")
dlg.addField("How long each word appears (sec):", 2.0)
dlg.addField("Time the '+' stays on screen (sec between each word):", 0.5)
dlg.addText("Which word types should be shown?")
include_neutral = dlg.addField("Everyday objects (e.g., table)", True)
include_aggression = dlg.addField("Aggressive words (e.g., punch)", True)
include_positive = dlg.addField("Positive words (e.g., love)", True)
include_negative = dlg.addField("Negative words (e.g., sad)", True)
include_color = dlg.addField("Color words (e.g., purple)", False)

ok_data = dlg.show()
if not dlg.OK:
    core.quit()

# === EXTRACT CONFIGURATION ===
participant_id = ok_data[0]
session_number = ok_data[1]
stim_time = float(ok_data[2])
fixation_time = float(ok_data[3])

selected_categories = {}
if ok_data[4]: selected_categories['neutral'] = categories['neutral']
if ok_data[5]: selected_categories['aggression'] = categories['aggression']
if ok_data[6]: selected_categories['positive'] = categories['positive']
if ok_data[7]: selected_categories['negative'] = categories['negative']
if ok_data[8]: selected_categories['color'] = categories['color']

# === SETUP WINDOW AND STIMULI ===
win = visual.Window(size=(800, 600), color='black', units='pix')
fixation = visual.TextStim(win, text='+', color='white')
stimulus = visual.TextStim(win, text='', color='white', height=50)
instruction = visual.TextStim(win, text='', color='white', height=30, wrapWidth=700)

clock = core.Clock()
results = []

# === INSTRUCTIONS ===
def show_instructions():
    heading = visual.TextStim(win, text="Instructions", color='white', height=60, pos=(0, 250))
    heading.draw()
    win.flip()
    core.wait(1.5)

    instruction.text = (
        "Hello!\n\n"
        "You will see words in different COLORS.\n"
        "Don't read the word—just look at the COLOR it's written in.\n\n"
        "Press the button that matches the COLOR.\n\n"
        "Let's see some examples!"
    )
    instruction.height = 30
    instruction.pos = (0, 100)
    instruction.draw()
    win.flip()
    event.waitKeys()

    # Image examples (use your own images)
    example_images = ['example1.png', 'example2.png']
    for img_file in example_images:
        image = visual.ImageStim(win, image=img_file, size=(600, 400))
        image.draw()
        win.flip()
        event.waitKeys()

    instruction.text = (
        "Great!\n\n"
        "- Look at the COLOR\n"
        "- Press the matching key\n"
        "- Try to be quick and right!\n\n"
        "Press any key to start practice."
    )
    instruction.pos = (0, 0)
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

instruction.text = "Great job! Now the main task will begin.\n\nPress any key to continue."
instruction.draw()
win.flip()
event.waitKeys()

start_time = core.getTime()
run_main()
end_time = core.getTime()
duration = round(end_time - start_time, 2)

save_data(duration)

instruction.text = f"Thank you! You're done!\nTotal Time: {duration} seconds.\nPress any key to close."
instruction.draw()
win.flip()
event.waitKeys()

win.close()
core.quit()
