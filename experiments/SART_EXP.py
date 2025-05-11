# --- SART Experiment (Modified for Faster Practice) ---
from psychopy import visual, core, event, gui, data
import random
import os

# --- 1. Participant Info ---
expInfo = {
    'Participant ID': '',
    'Session': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],  # Dropdown menu
    'Show Instructions': True,  # Toggle for instructions
    'Practice Trials': True,    # Toggle for practice
    'Number of Practice Trials': 5,  # How many practice trials
    'Number of Main Trials': 90,     # How many main trials
    'Stimulus Duration (sec)': 0.35, # How long each number shows
    'Break Duration (sec)': 0.5      # Time between numbers
}

dlg = gui.DlgFromDict(expInfo, title="SART Experiment", 
                     order=['Participant ID', 'Session', 'Show Instructions', 'Practice Trials', 
                           'Number of Practice Trials', 'Number of Main Trials', 
                           'Stimulus Duration (sec)', 'Break Duration (sec)'])
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
    
    filename = os.path.join(data_dir, f"SART_{expInfo['Participant ID']}_{expInfo['Session']}")
    thisExp = data.ExperimentHandler(dataFileName=filename)
except Exception as e:
    print(f"Error setting up data directory: {str(e)}")
    core.quit()

# --- 3. Experiment Parameters ---
stim_duration = expInfo['Stimulus Duration (sec)']
isi_duration = expInfo['Break Duration (sec)']
target_number = '3'    # number to withhold response
practice_trials = expInfo['Number of Practice Trials']
main_trials = expInfo['Number of Main Trials']

# --- 4. Create Window and Stimuli ---
win = visual.Window(fullscr=False, color='black')
fixation = visual.TextStim(win, text='+', color='white')
digit_stim = visual.TextStim(win, text='', color='white', height=0.2)
instruction_text = visual.TextStim(win, text='', color='white', wrapWidth=1.5)
feedback_text = visual.TextStim(win, text='', color='white', height=0.1)

# --- 5. Show Instructions ---
if expInfo['Show Instructions']:
    instructions = (
        "Welcome to the Number Game!\n\n"
        "Here's how to play:\n"
        "• Numbers will flash on the screen\n"
        "• Press SPACEBAR for EVERY number...\n"
        "• ...EXCEPT when you see the number 3!\n\n"
        "For example:\n"
        "• See 1, 2, 4, 5, 6, 7, 8, 9, 0? → Press SPACEBAR!\n"
        "• See 3? → Don't press anything!\n\n"
        "Ready to try? Press any key to start practice!"
    )

    instruction_text.text = instructions
    instruction_text.draw()
    win.flip()
    event.waitKeys()

# --- 6. Practice Trials ---
if expInfo['Practice Trials']:
    digits = [str(i) for i in range(10)]
    practice_list = random.choices(digits, k=practice_trials)

    for trial_num, digit in enumerate(practice_list):
        # Show fixation
        fixation.draw()
        win.flip()
        core.wait(isi_duration)

        # Show digit
        digit_stim.text = digit
        digit_stim.draw()
        win.flip()
        core.wait(stim_duration)

        # Collect response
        keys = event.getKeys(keyList=['space', 'escape'], timeStamped=True)

        responded = any(k[0] == 'space' for k in keys)
        correct = (digit != target_number and responded) or (digit == target_number and not responded)

        # Feedback
        if correct:
            feedback_text.text = "Great job!"
        else:
            if digit == target_number:
                feedback_text.text = "Remember: Don't press for 3!"
            else:
                feedback_text.text = "Oops! Press SPACEBAR for other numbers!"
        
        feedback_text.draw()
        win.flip()
        core.wait(0.75)

        if any(k[0] == 'escape' for k in keys):
            core.quit()

# --- 7. Start Main Experiment Instructions ---
instruction_text.text = (
    "Now for the real game!\n\n"
    "• Press SPACEBAR for all numbers except 3\n"
    "• Try to be quick but accurate\n"
    "• Take a deep breath and focus\n\n"
    "Ready? Press any key to begin!"
)
instruction_text.draw()
win.flip()
event.waitKeys()

# --- 8. Main Trials (same speed) ---
main_list = random.choices(digits, k=main_trials)

for trial_num, digit in enumerate(main_list):
    # Show fixation
    fixation.draw()
    win.flip()
    core.wait(isi_duration)

    # Show digit
    digit_stim.text = digit
    digit_stim.draw()
    win.flip()
    core.wait(stim_duration)

    # Collect response
    keys = event.getKeys(keyList=['space', 'escape'], timeStamped=True)

    responded = any(k[0] == 'space' for k in keys)
    correct = (digit != target_number and responded) or (digit == target_number and not responded)

    # Save data
    thisExp.addData('trial', trial_num)
    thisExp.addData('digit', digit)
    thisExp.addData('responded', responded)
    thisExp.addData('correct', correct)
    if keys:
        thisExp.addData('response_time', keys[0][1])  # first key press time
    else:
        thisExp.addData('response_time', '')

    thisExp.nextEntry()

    if any(k[0] == 'escape' for k in keys):
        core.quit()

# --- 9. Goodbye Screen ---
instruction_text.text = (
    "All done! Thank you for playing!\n\n"
    "You did a great job with the numbers!\n"
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
