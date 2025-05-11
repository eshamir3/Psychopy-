# --- Value Choice Experiment ---
from psychopy import visual, core, event, gui, data
import random
import os

# --- 1. Participant Info ---
expInfo = {
    'Participant ID': '',
    'Session': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],  # Dropdown menu
    'Show Instructions': True,  # Toggle for instructions
    'Practice Trials': True,    # Toggle for practice
    'Trial Duration (sec)': 5.0  # How long each choice stays on screen
}

dlg = gui.DlgFromDict(expInfo, title="Value Choice Experiment", 
                     order=['Participant ID', 'Session', 'Show Instructions', 'Practice Trials', 'Trial Duration (sec)'])
if not dlg.OK:
    core.quit()

# --- 2. Data file setup ---
try:
    # Get the absolute path to the data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(parent_dir, 'data')
    
    # Create data directory if it doesn't exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    filename = os.path.join(data_dir, f"VALUECHOICE_{expInfo['Participant ID']}_{expInfo['Session']}")
    thisExp = data.ExperimentHandler(dataFileName=filename)
except Exception as e:
    print(f"Error setting up data directory: {str(e)}")
    core.quit()

# --- 3. Create Window and Stimuli ---
win = visual.Window(size=(1024, 768), color="white", units="pix", fullscr=False)
instruction_text = visual.TextStim(win, text='', color='black', wrapWidth=800)
left_text = visual.TextStim(win, text='', pos=(-300, 0), color='black', wrapWidth=400)
right_text = visual.TextStim(win, text='', pos=(300, 0), color='black', wrapWidth=400)
feedback_text = visual.TextStim(win, text='', color='green', wrapWidth=800)

# --- 4. Define stimulus pairs ---
stim_pairs = [
    ("Receive $10 today", "Receive $15 in one week"),
    ("Work 2 hours for $20", "Work 1 hour for $8"),
    ("Buy 1 item at $10", "Buy 2 items at $18"),
    ("Walk 30 minutes to save $3", "Pay full price for convenience"),
    ("Donate $5 to a local charity", "Keep the $5 for yourself")
]
random.shuffle(stim_pairs)

# --- 5. Show Instructions ---
if expInfo['Show Instructions']:
    instructions = (
        "Welcome to the Value Choice Game!\n\n"
        "You'll see two choices on the screen:\n"
        "• LEFT side: Press the LEFT arrow key\n"
        "• RIGHT side: Press the RIGHT arrow key\n\n"
        "Choose what you think is best!\n"
        "There are no wrong answers - just pick what you prefer.\n\n"
        "Ready to try? Press SPACE to start!"
    )

    instruction_text.text = instructions
    instruction_text.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

# --- 6. Practice Trial ---
if expInfo['Practice Trials']:
    practice_pair = ("Receive $10 today", "Receive $15 in one week")
    left_text.text = practice_pair[0]
    right_text.text = practice_pair[1]

    instruction_text.text = "Let's practice! Choose one option:"
    instruction_text.draw()
    left_text.draw()
    right_text.draw()
    win.flip()
    practice_keys = event.waitKeys(keyList=['left', 'right'])

    practice_choice = practice_pair[0] if 'left' in practice_keys else practice_pair[1]
    feedback_text.text = f"Great choice! You picked:\n{practice_choice}\n\nPress SPACE to continue!"
    feedback_text.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

# --- 7. Pre-experiment Prompt ---
instruction_text.text = (
    "Now for the real game!\n\n"
    "• You'll see 5 different choices\n"
    "• Take your time to think\n"
    "• Choose what feels right to you\n\n"
    "Ready? Press SPACE to start!"
)
instruction_text.draw()
win.flip()
event.waitKeys(keyList=['space'])

# --- 8. Main Trials ---
for i, (stim1, stim2) in enumerate(stim_pairs):
    left_text.text = stim1
    right_text.text = stim2

    left_text.draw()
    right_text.draw()
    win.flip()

    start_time = core.getTime()
    keys = event.waitKeys(keyList=['left', 'right', 'escape'])
    rt = round(core.getTime() - start_time, 3)

    if 'escape' in keys:
        break

    choice = stim1 if 'left' in keys else stim2

    # Save data
    thisExp.addData('trial', i + 1)
    thisExp.addData('stim1', stim1)
    thisExp.addData('stim2', stim2)
    thisExp.addData('choice', choice)
    thisExp.addData('reaction_time', rt)
    thisExp.nextEntry()

# --- 9. Goodbye Screen ---
instruction_text.text = (
    "All done! Thank you for playing!\n\n"
    "You did a great job making choices.\n"
    "You may now close the window."
)
instruction_text.draw()
win.flip()
core.wait(3.0)

# --- 10. Save and Exit ---
try:
    thisExp.saveAsWideText(filename + '.csv')
    # Show success message
    instruction_text.text = f"Data saved successfully to:\n{filename}.csv\n\nYou may now close the window."
    instruction_text.draw()
    win.flip()
    core.wait(3.0)
except Exception as e:
    # Show error message if saving fails
    instruction_text.text = f"Error saving data: {str(e)}\n\nPress any key to exit."
    instruction_text.draw()
    win.flip()
    event.waitKeys()

win.close()
core.quit() 