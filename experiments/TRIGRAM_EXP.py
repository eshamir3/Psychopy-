# --- Consonant Trigram Task (Complete Version) ---
from psychopy import visual, core, event, gui
import random, string, csv, os
import argparse

# --- Parse command-line arguments ---
parser = argparse.ArgumentParser()
parser.add_argument('--participant_id', type=str, default='test_subject')
parser.add_argument('--session', type=str, default='1')
parser.add_argument('--show_instructions', type=str, default='True')
parser.add_argument('--practice_trials', type=str, default='True')
parser.add_argument('--number_of_practice_trials', type=str, default='3')
parser.add_argument('--number_of_main_trials', type=str, default='6')
parser.add_argument('--trigram_duration_sec', type=str, default='1.5')
parser.add_argument('--countdown_step', type=str, default='3')
parser.add_argument('--input_timeout_sec', type=str, default='10.0')
args, unknown = parser.parse_known_args()

# --- Build expInfo dict from args ---
expInfo = {
    'Participant ID': args.participant_id,
    'Session': args.session,
    'Show Instructions': args.show_instructions.lower() in ('true', '1', 'yes'),
    'Practice Trials': args.practice_trials.lower() in ('true', '1', 'yes'),
    'Number of Practice Trials': int(args.number_of_practice_trials),
    'Number of Main Trials': int(args.number_of_main_trials),
    'Trigram Duration (sec)': float(args.trigram_duration_sec),
    'Countdown Step': int(args.countdown_step),
    'Input Timeout (sec)': float(args.input_timeout_sec)
}

# --- Assign Parameters ---
participant_id     = expInfo['Participant ID'].strip() or "unknown"
session_id         = expInfo['Session']
trigram_dur        = float(expInfo['Trigram Duration (sec)'])
count_step         = int(expInfo['Countdown Step'])
input_timeout      = float(expInfo['Input Timeout (sec)'])
n_practice         = int(expInfo['Number of Practice Trials'])
n_main             = int(expInfo['Number of Main Trials'])
show_instructions  = expInfo['Show Instructions']
run_practice       = expInfo['Practice Trials']
recall_delays      = [3, 6, 9]

# --- Constants ---
instruction_dur = 2.5
countdown_dur   = 1.0
feedback_dur    = 2.0
iti             = 3.0

# --- Setup Window and Stimuli ---
win = visual.Window(fullscr=False, color='white', units='height')
text_stim = visual.TextStim(win, text='', color='black', height=0.07, wrapWidth=1.2)
prompt_stim = visual.TextStim(win, text="Type the three letters you remembered and press ENTER", pos=(0, -0.2), color='black', height=0.05)
instruction_stim = visual.TextStim(win, text='', color='black', height=0.06, wrapWidth=1.2)
feedback_stim = visual.TextStim(win, text='', color='black', height=0.06, wrapWidth=1.2)

# --- Helper Functions ---
def show_text(msg, wait_keys=True):
    text_stim.text = msg
    text_stim.draw()
    win.flip()
    if wait_keys:
        event.waitKeys()

def generate_trigram():
    consonants = [c for c in string.ascii_uppercase if c not in 'AEIOUY']
    return ''.join(random.sample(consonants, 3))

def generate_start_number():
    return random.randint(300, 999)

def get_trigram(timeout=input_timeout, max_len=3):
    response = ""
    event.clearEvents(eventType='keyboard')
    clock = core.Clock()

    while clock.getTime() < timeout:
        cursor = "|" if (int(clock.getTime() * 2) % 2 == 0) else ""
        text_stim.text = response + cursor
        text_stim.draw()
        prompt_stim.draw()
        win.flip()

        keys = event.getKeys()
        for key in keys:
            if key in list(string.ascii_letters) and len(response) < max_len:
                response += key.upper()
            elif key == 'backspace':
                response = response[:-1]
            elif key in ['return', 'enter']:
                return response
    return response

def run_trial(is_practice=False):
    trigram = generate_trigram()
    start_num = generate_start_number()
    delay = random.choice(recall_delays)

    # Show trigram
    text_stim.text = trigram
    text_stim.draw()
    win.flip()
    core.wait(trigram_dur)

    # Countdown instruction
    text_stim.text = f"Count backwards by {count_step}\nFrom: {start_num}"
    text_stim.draw()
    win.flip()
    core.wait(instruction_dur)

    # Countdown display
    current = start_num
    for _ in range(delay):
        current -= count_step
        text_stim.text = str(current)
        text_stim.draw()
        win.flip()
        core.wait(countdown_dur)

    # Input response
    response = get_trigram(timeout=input_timeout, max_len=3)
    correct = (response == trigram)

    # Feedback (for practice only)
    if is_practice:
        feedback_stim.text = "Correct!" if correct else f"Incorrect.\nCorrect was: {trigram}"
        feedback_stim.draw()
        win.flip()
        core.wait(feedback_dur)

    core.wait(iti)
    return trigram, response, correct

# --- Instructions ---
if show_instructions:
    instruction_stim.text = (
        "1. You will see 3 capital letters (e.g., DKT).\n"
        "2. Try to memorize them in the exact order.\n"
        "3. You will then be shown a number (e.g., 300).\n"
        "4. Count backward by the specified amount (e.g., by 3s: 300, 297, 294...).\n"
        "5. After the countdown, you'll be asked to TYPE the original letters.\n"
        "6. Type the letters exactly as you saw them and press ENTER.\n"
        "7. You have a limited time to type your response.\n\n"
        "Press any key to begin practice!"
    )
    instruction_stim.draw()
    win.flip()
    event.waitKeys()

# --- Practice Trials ---
if run_practice:
    for _ in range(n_practice):
        tri, resp, corr = run_trial(is_practice=True)
        feedback_stim.text = "Well done!" if corr else "Try to focus more on the letters."
        feedback_stim.draw()
        win.flip()
        core.wait(1.0)

# --- Pre-Main Trial Message ---
avg_delay = sum(recall_delays) / len(recall_delays)
estimated_time = ((trigram_dur + instruction_dur + avg_delay * countdown_dur + input_timeout + iti) * n_main) / 60
instruction_stim.text = (
    f"Now begins the main task.\n\n"
    f"You will complete {n_main} trials.\n"
    f"Estimated time: {int(estimated_time) + 1} minutes.\n\n"
    f"Remember to:\n"
    f"- Type the letters exactly as you saw them\n"
    f"- Press ENTER after typing\n"
    f"- Stay focused and try your best\n\n"
    f"Press any key to begin."
)
instruction_stim.draw()
win.flip()
event.waitKeys()

# --- Main Trials ---
results = []
for t in range(1, n_main + 1):
    tri, resp, corr = run_trial(is_practice=False)
    results.append((participant_id, session_id, t, tri, resp, corr))

# --- Save Data ---
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(parent_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)

    filename = os.path.join(data_dir, f"TRIGRAM_{participant_id}_S{session_id}.csv")
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['participant', 'session', 'trial', 'trigram', 'response', 'correct'])
        writer.writerows(results)

    instruction_stim.text = "Task complete. Thank you!\n\nYour responses have been saved."
    instruction_stim.draw()
    win.flip()
    core.wait(3.0)
except Exception as e:
    show_text(f"Error saving data:\n{str(e)}\n\nPress any key to exit.")

win.close()
core.quit()
