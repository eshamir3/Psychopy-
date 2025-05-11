# --- Go/No-Go Task Experiment ---
from psychopy import visual, core, event, gui, data
import random
import os

# --- 1. Participant Info ---
expInfo = {
    'Participant ID': '',
    'Session': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],  # Dropdown menu
    'Show Instructions': True,  # Toggle for instructions
    'Practice Trials': True,    # Toggle for practice
    'Number of Practice Trials': 10,  # How many practice trials
    'Number of Main Trials': 100,     # How many main trials
    'Stimulus Duration (sec)': 0.5,   # How long each letter shows
    'Response Window (sec)': 1.0,     # Time allowed to respond
    'ITI Duration (sec)': 0.5         # Time between trials
}

dlg = gui.DlgFromDict(expInfo, title="Go/No-Go Task", 
                     order=['Participant ID', 'Session', 'Show Instructions', 'Practice Trials', 
                           'Number of Practice Trials', 'Number of Main Trials', 
                           'Stimulus Duration (sec)', 'Response Window (sec)', 'ITI Duration (sec)'])
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
    
    filename = os.path.join(data_dir, f"GONOGO_{expInfo['Participant ID']}_{expInfo['Session']}")
    thisExp = data.ExperimentHandler(dataFileName=filename)
except Exception as e:
    print(f"Error setting up data directory: {str(e)}")
    core.quit()

# --- 3. Create Window and Stimuli ---
win = visual.Window(size=(1024, 768), color="white", units="pix", fullscr=False)
instruction_text = visual.TextStim(win, text='', color='black', wrapWidth=800)
stimulus_text = visual.TextStim(win, text='', color='black', height=0.2)
feedback_text = visual.TextStim(win, text='', color='green', wrapWidth=800)
fixation = visual.TextStim(win, text='+', color='black', height=0.1)

# --- 4. Define trial types ---
# Go trials (press space)
go_trials = ['X', 'Y', 'Z']

# No-Go trials (don't press)
nogo_trials = ['A', 'B', 'C']

# --- 5. Show Instructions ---
if expInfo['Show Instructions']:
    instructions = (
        "Welcome to the Letter Game!\n\n"
        "Here's how to play:\n"
        "• You'll see letters appear on screen\n"
        "• Press SPACEBAR for X, Y, or Z\n"
        "• Do NOT press for A, B, or C\n\n"
        "Ready to try? Press any key to start practice!"
    )

    instruction_text.text = instructions
    instruction_text.draw()
    win.flip()
    event.waitKeys()

# --- 6. Practice Trials ---
if expInfo['Practice Trials']:
    practice_trials = (go_trials * 2 + nogo_trials)  # More Go trials for practice
    random.shuffle(practice_trials)

    for trial in practice_trials:
        # Show fixation
        fixation.draw()
        win.flip()
        core.wait(expInfo['ITI Duration (sec)'])

        # Show stimulus
        stimulus_text.text = trial
        stimulus_text.draw()
        win.flip()
        
        # Collect response
        start_time = core.getTime()
        keys = event.waitKeys(keyList=['space', 'escape'], 
                            maxWait=expInfo['Response Window (sec)'])
        rt = core.getTime() - start_time

        if 'escape' in keys:
            core.quit()

        # Feedback
        if trial in go_trials:
            if keys and 'space' in keys:
                feedback_text.text = "Great job!"
            else:
                feedback_text.text = "Remember: Press SPACEBAR for X, Y, or Z!"
        else:  # No-Go trial
            if not keys:
                feedback_text.text = "Great job!"
            else:
                feedback_text.text = "Remember: Don't press for A, B, or C!"
        
        feedback_text.draw()
        win.flip()
        core.wait(0.75)

# --- 7. Start Main Experiment Instructions ---
instruction_text.text = (
    "Now for the real game!\n\n"
    "• Press SPACEBAR for X, Y, or Z\n"
    "• Do NOT press for A, B, or C\n"
    "• Try to be quick but accurate\n"
    "• Take a deep breath and focus\n\n"
    "Ready? Press any key to begin!"
)
instruction_text.draw()
win.flip()
event.waitKeys()

# --- 8. Main Trials ---
main_trials = (go_trials * (expInfo['Number of Main Trials'] // 2) +
              nogo_trials * (expInfo['Number of Main Trials'] // 2))
random.shuffle(main_trials)

for i, trial in enumerate(main_trials):
    # Show fixation
    fixation.draw()
    win.flip()
    core.wait(expInfo['ITI Duration (sec)'])

    # Show stimulus
    stimulus_text.text = trial
    stimulus_text.draw()
    win.flip()
    
    # Collect response
    start_time = core.getTime()
    keys = event.waitKeys(keyList=['space', 'escape'], 
                        maxWait=expInfo['Response Window (sec)'])
    rt = core.getTime() - start_time

    if 'escape' in keys:
        break

    # Save data
    thisExp.addData('trial', i + 1)
    thisExp.addData('stimulus', trial)
    thisExp.addData('trial_type', 'go' if trial in go_trials else 'nogo')
    thisExp.addData('response', 'space' if keys and 'space' in keys else '')
    thisExp.addData('rt', rt if keys else '')
    thisExp.addData('correct', int((trial in go_trials and keys and 'space' in keys) or 
                                 (trial in nogo_trials and not keys)))
    thisExp.nextEntry()

# --- 9. Goodbye Screen ---
instruction_text.text = (
    "All done! Thank you for playing!\n\n"
    "You did a great job with the letters!\n"
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