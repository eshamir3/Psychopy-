# Consonant Trigram Task in PsychoPy
# Now records a participant ID and names the output file "{participant_id}.csv"
# Requirements: psychopy installed (`pip install psychopy`)

from psychopy import visual, core, event, gui
import random, string, csv

# ============ GET PARTICIPANT ID ============
dlg = gui.Dlg(title="Participant Info")
dlg.addField("Participant ID:")
if not dlg.show():
    core.quit()  # user hit cancel
participant_id = dlg.data[0].strip()
if not participant_id:
    participant_id = "unknown"

# ============ CONFIGURATION ============
trigram_duration     = 1.5       # seconds to show the trigram
instruction_duration = 2.5       # seconds to show the "Count backwards…" instruction
prompt_duration      = 1.0       # seconds per countdown step
feedback_duration    = 2.0       # seconds to show practice feedback
iti                  = 3.0       # inter-trial interval
backward_step        = 3         # how much to count down each step
input_timeout        = 10.0      # max seconds to type your response

practice_trials      = 3
main_trials          = 6         # e.g. 48 in a full study
recall_delays        = [3, 6, 9] # seconds of backward counting

# ============ SETUP WINDOW & STIMULI ============
win = visual.Window(fullscr=False, color='white', units='height')
text_stim   = visual.TextStim(win, text='', color='black', height=0.07, wrapWidth=1.2)
prompt_stim = visual.TextStim(win,
                              text="Type trigram and press ENTER",
                              pos=(0, -0.2),
                              color='black',
                              height=0.05)

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
show_text(
    "Welcome to the Consonant Trigram Task.\n\n"
    "You will see 3 letters, then count backwards,\n"
    "and then type the letters you saw.\n\n"
    "Press any key to start PRACTICE."
)
for _ in range(practice_trials):
    run_trial(is_practice=True)

# Estimate total duration
avg_delay      = sum(recall_delays) / len(recall_delays)
per_trial_time = (trigram_duration +
                  instruction_duration +
                  avg_delay +
                  input_timeout +
                  iti)
est_minutes    = int((per_trial_time * main_trials) / 60) + 1

show_text(
    f"Practice done! No feedback in the main test.\n\n"
    f"Estimated duration: {est_minutes} minutes.\n\n"
    "Press any key to begin."
)

# Main experiment
results = []
for t in range(1, main_trials + 1):
    tri, resp, corr = run_trial(is_practice=False)
    results.append((participant_id, t, tri, resp, corr))

# ==== SAVE DATA TO "{participant_id}.csv" ====
filename = f"{participant_id}.csv"
with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['participant','trial','trigram','response','correct'])
    writer.writerows(results)

# End screen
show_text("You have completed the task.\n\nThank you for participating!\n\nPress any key to exit.")

win.close()
core.quit()
