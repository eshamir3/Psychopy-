# --- Value Choice Experiment with Clickable Cards ---
from psychopy import visual, core, event, gui, data
import random
import os

# --- 1. Participant Info and Parameters ---
expInfo = {
    'Participant ID': '',
    'Session': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
    'Show Instructions': True,
    'Practice Trials': True,
    'Trial Duration (sec)': 5.0,
    'Feedback Duration (sec)': 2.0,
    'Randomize Position': True,
    '# of Trials': ['5', '10', '15']
}
dlg = gui.DlgFromDict(expInfo, title="Value Choice Experiment", 
                     order=['Participant ID', 'Session', 'Show Instructions', 'Practice Trials', 
                            'Trial Duration (sec)', 'Feedback Duration (sec)', 
                            'Randomize Position', '# of Trials'])
if not dlg.OK:
    core.quit()

num_trials = int(expInfo['# of Trials'])

# --- 2. Data file setup ---
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(parent_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    filename = os.path.join(data_dir, f"VALUECHOICE_{expInfo['Participant ID']}_{expInfo['Session']}")
    thisExp = data.ExperimentHandler(dataFileName=filename)
except Exception as e:
    print(f"Error setting up data directory: {str(e)}")
    core.quit()

# --- 3. Create Window and Stimuli ---
win = visual.Window(size=(1024, 768), color="white", units="pix", fullscr=False)
instruction_text = visual.TextStim(win, text='', color='black', wrapWidth=800)
feedback_text = visual.TextStim(win, text='', color='green', wrapWidth=800)
mouse_obj = event.Mouse(win=win)

# --- 4. Define stimulus pairs ---
stim_pairs = [
    ("Receive $10 today", "Receive $15 in one week"),
    ("Work 2 hours for $20", "Work 1 hour for $8"),
    ("Buy 1 item at $10", "Buy 2 items at $18"),
    ("Walk 30 minutes to save $3", "Pay full price for convenience"),
    ("Donate $5 to a local charity", "Keep the $5 for yourself"),
    ("Exercise 20 mins today", "Relax now, exercise tomorrow"),
    ("Cook at home", "Order delivery for $5 more"),
    ("Read 10 pages", "Watch a short video"),
    ("Clean your desk now", "Leave it for later"),
    ("Call a friend", "Send a text instead"),
    ("Sleep early", "Stay up and watch a movie"),
    ("Save $10", "Buy a small treat"),
    ("Volunteer 1 hour", "Relax with a show"),
    ("Invest $50", "Spend $50 on fun"),
    ("Spend time offline", "Browse social media")
]
random.shuffle(stim_pairs)
stim_pairs = stim_pairs[:num_trials]  # Trim to desired trial count

# --- 5. Card setup ---
card_width, card_height = 500, 300
left_card = visual.Rect(win, width=card_width, height=card_height, pos=(-300, 0), fillColor='lightgrey', lineColor='black')
right_card = visual.Rect(win, width=card_width, height=card_height, pos=(300, 0), fillColor='lightgrey', lineColor='black')
left_text = visual.TextStim(win, text='', pos=(-300, 0), color='black', wrapWidth=400)
right_text = visual.TextStim(win, text='', pos=(300, 0), color='black', wrapWidth=400)

def display_cards(text1, text2):
    left_card.draw()
    right_card.draw()
    left_text.text = text1
    right_text.text = text2
    left_text.draw()
    right_text.draw()
    win.flip()

def get_card_clicked():
    mouse_obj.clickReset()
    timer = core.Clock()
    while timer.getTime() < float(expInfo['Trial Duration (sec)']):
        if mouse_obj.isPressedIn(left_card):
            return 'left', timer.getTime()
        elif mouse_obj.isPressedIn(right_card):
            return 'right', timer.getTime()
    return 'none', float(expInfo['Trial Duration (sec)'])

# --- 6. Instructions ---
if expInfo['Show Instructions']:
    instruction_text.text = (
        "Welcome to the Value Choice Game!\n\n"
        "You’ll see two cards, each with a different option.\n"
        "Click on the card you prefer using your mouse.\n\n"
        "There are no right or wrong answers.\n\n"
        "When you're ready, press SPACE to start!"
    )
    instruction_text.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

# --- 7. Practice Trial ---
if expInfo['Practice Trials']:
    practice_pair = ("Receive $10 today", "Receive $15 in one week")
    instruction_text.text = "Let's practice! Click the card you prefer."
    instruction_text.draw()
    win.flip()
    core.wait(1)
    display_cards(*practice_pair)
    side, rt = get_card_clicked()
    choice = practice_pair[0] if side == 'left' else practice_pair[1] if side == 'right' else 'No response'
    feedback_text.text = f"You picked:\n{choice}\n\nNice! Press SPACE to continue."
    feedback_text.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

# --- 8. Ready Message ---
instruction_text.text = (
    f"Now it's time for the real choices.\n\n"
    f"There will be {num_trials} trials.\n"
    "Take your time, and click on what feels right.\n\n"
    "Press SPACE to begin."
)
instruction_text.draw()
win.flip()
event.waitKeys(keyList=['space'])

# --- 9. Main Trials ---
for i, (stim1, stim2) in enumerate(stim_pairs):
    if expInfo['Randomize Position'] and random.choice([True, False]):
        left_stim, right_stim = stim2, stim1
    else:
        left_stim, right_stim = stim1, stim2

    display_cards(left_stim, right_stim)
    side, rt = get_card_clicked()

    if side == 'none':
        choice = 'No response'
    else:
        choice = left_stim if side == 'left' else right_stim

    # Log data
    thisExp.addData('trial', i + 1)
    thisExp.addData('left_option', left_stim)
    thisExp.addData('right_option', right_stim)
    thisExp.addData('choice', choice)
    thisExp.addData('side_chosen', side)
    thisExp.addData('reaction_time', round(rt, 3))
    thisExp.nextEntry()

    # Show feedback
    feedback_text.text = f"You picked:\n{choice}"
    feedback_text.draw()
    win.flip()
    core.wait(float(expInfo['Feedback Duration (sec)']))

# --- 10. Goodbye ---
instruction_text.text = "Thank you! Your responses have been recorded.\n\nYou may now close the window."
instruction_text.draw()
win.flip()
core.wait(3)

try:
    thisExp.saveAsWideText(filename + '.csv')
except Exception as e:
    instruction_text.text = f"Error saving data: {str(e)}\nPress any key to exit."
    instruction_text.draw()
    win.flip()
    event.waitKeys()

win.close()
core.quit()
