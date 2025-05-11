# Consonant Trigram Task in PsychoPy
# Now records a participant ID and names the output file "{participant_id}.csv"
# Requirements: psychopy installed (`pip install psychopy`)

from psychopy import visual, core, event, gui
import random, string, csv
import os

# ============ GET PARTICIPANT INFO ============
expInfo = {
    'Participant ID': '',
    'Session': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],  # Dropdown menu
    'Show Instructions': True,  # Toggle for instructions
    'Practice Trials': True,    # Toggle for practice
    'Number of Practice Trials': 3,  # How many practice trials
    'Number of Main Trials': 6,      # How many main trials
    'Trigram Duration (sec)': 1.5,   # How long to show letters
    'Countdown Step': 3,             # How much to count down by
    'Input Timeout (sec)': 10.0      # Max time to type response
}

dlg = gui.DlgFromDict(expInfo, title="Letter Memory Game", 
                     order=['Participant ID', 'Session', 'Show Instructions', 'Practice Trials', 
                           'Number of Practice Trials', 'Number of Main Trials', 
                           'Trigram Duration (sec)', 'Countdown Step', 'Input Timeout (sec)'])
if not dlg.OK:
    core.quit()

participant_id = expInfo['Participant ID'].strip()
if not participant_id:
    participant_id = "unknown"

# ============ CONFIGURATION ============
trigram_duration     = expInfo['Trigram Duration (sec)']
instruction_duration = 2.5       # seconds to show the "Count backwards…" instruction
prompt_duration      = 1.0       # seconds per countdown step
feedback_duration    = 2.0       # seconds to show practice feedback
iti                  = 3.0       # inter-trial interval
backward_step        = expInfo['Countdown Step']
input_timeout        = expInfo['Input Timeout (sec)']

practice_trials      = expInfo['Number of Practice Trials']
main_trials          = expInfo['Number of Main Trials']
recall_delays        = [3, 6, 9] # seconds of backward counting

# ============ SETUP WINDOW & STIMULI ============
win = visual.Window(fullscr=False, color='white', units='height')
text_stim   = visual.TextStim(win, text='', color='black', height=0.07, wrapWidth=1.2)
prompt_stim = visual.TextStim(win,
                              text="Type trigram and press ENTER",
                              pos=(0, -0.2),
                              color='black',
                              height=0.05)
instruction_text = visual.TextStim(win, text='', color='black', height=0.07, wrapWidth=1.2)
feedback_text = visual.TextStim(win, text='', color='black', height=0.07, wrapWidth=1.2)

# ============ HELPER FUNCTIONS ============

def show_text(txt, wait_keys=True):
    text_stim.text = txt
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
        cursor = "|" if (int(clock.getTime() * 2) % 2) == 0 else ""
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

    return response  # timeout

def run_trial(is_practice=False):
    trigram   = generate_trigram()
    start_num = generate_start_number()
    delay     = random.choice(recall_delays)

    # 1) Show the trigram
    text_stim.text = trigram
    text_stim.draw()
    win.flip()
    core.wait(trigram_duration)

    # 2) Show countdown instruction
    text_stim.text = f"Count backwards by {backward_step}\nFrom: {start_num}"
    text_stim.draw()
    win.flip()
    core.wait(instruction_duration)

    # 3) Countdown prompts
    current = start_num
    for _ in range(int(delay)):
        current -= backward_step
        text_stim.text = str(current)
        text_stim.draw()
        win.flip()
        core.wait(prompt_duration)

    # 4) Collect recall response
    response = get_trigram(timeout=input_timeout, max_len=3)

    # 5) Practice feedback
    correct = (response == trigram)
    if is_practice:
        fb = "Correct!" if correct else f"Incorrect. The correct trigram was {trigram}"
        show_text(fb, wait_keys=False)
        core.wait(feedback_duration)

    core.wait(iti)
    return trigram, response, correct

# ============ RUN THE TASK ============

# Instructions & practice
if expInfo['Show Instructions']:
    instructions = (
        "Welcome to the Letter Memory Game!\n\n"
        "Here's how to play:\n"
        "• You'll see 3 letters appear\n"
        "• Try to remember them\n"
        "• Then count backwards from 100 by 3\n"
        "• Finally, type the letters you saw\n\n"
        "Ready to try? Press any key to start practice!"
    )

    instruction_text.text = instructions
    instruction_text.draw()
    win.flip()
    event.waitKeys()

if expInfo['Practice Trials']:
    for _ in range(practice_trials):
        tri, resp, corr = run_trial(is_practice=True)
        # Feedback
        if corr:
            feedback_text.text = "Great job!"
        else:
            feedback_text.text = "Remember to type all three letters!"
        
        feedback_text.draw()
        win.flip()
        core.wait(0.75)

        if any(k[0] == 'escape' for k in keys):
            core.quit()

# Estimate total duration
avg_delay      = sum(recall_delays) / len(recall_delays)
per_trial_time = (trigram_duration +
                  instruction_duration +
                  avg_delay +
                  input_timeout +
                  iti)
est_minutes    = int((per_trial_time * main_trials) / 60) + 1

instruction_text.text = (
    "Now for the real game!\n\n"
    "• Remember the 3 letters\n"
    "• Count backwards by 3\n"
    "• Type the letters when asked\n"
    "• Take a deep breath and focus\n\n"
    "Ready? Press any key to begin!"
)
instruction_text.draw()
win.flip()
event.waitKeys()

# Main experiment
results = []
for t in range(1, main_trials + 1):
    tri, resp, corr = run_trial(is_practice=False)
    results.append((participant_id, t, tri, resp, corr))

# ==== SAVE DATA ====
try:
    # Get the absolute path to the data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(parent_dir, 'data')
    
    # Create data directory if it doesn't exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Save the data
    filename = os.path.join(data_dir, f"TRIGRAM_{participant_id}.csv")
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['participant','trial','trigram','response','correct'])
        writer.writerows(results)
    
    # Show success message
    instruction_text.text = (
        "All done! Thank you for playing!\n\n"
        "You did a great job with the letters!\n"
        "You may now close the window."
    )
    instruction_text.draw()
    win.flip()
    core.wait(3.0)
except Exception as e:
    # Show error message if saving fails
    show_text(
        f"Oops! Something went wrong: {str(e)}\n\n"
        "Please let the experimenter know.\n\n"
        "Press any key to exit."
    )

win.close()
core.quit()