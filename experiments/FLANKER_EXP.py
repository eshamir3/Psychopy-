# --- Flanker Task Experiment ---
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
    'Stimulus Duration (sec)': 0.5,   # How long each arrow shows
    'Response Window (sec)': 2.0,     # Time allowed to respond
    'ITI Duration (sec)': 0.5         # Time between trials
}

dlg = gui.DlgFromDict(expInfo, title="Flanker Task", 
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
    
    filename = os.path.join(data_dir, f"FLANKER_{expInfo['Participant ID']}_{expInfo['Session']}")
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
continue_text = visual.TextStim(win, text='Press SPACE to continue', color='black', pos=(0, -300))

# --- 4. Define trial types ---
# Congruent trials (arrows point same direction)
congruent_trials = [
    ('<<<<<', 'left'),
    ('>>>>>', 'right')
]

# Incongruent trials (center arrow points opposite to flankers)
incongruent_trials = [
    ('<<><<', 'right'),
    ('>><>>', 'left')
]

# --- 5. Show Instructions ---
if expInfo['Show Instructions']:
    instructions = (
        "Welcome to the Arrow Game!\n\n"
        "Here's how to play:\n"
        "• Look at the MIDDLE arrow\n"
        "• If it points LEFT, press the LEFT arrow key\n"
        "• If it points RIGHT, press the RIGHT arrow key\n"
        "• Ignore the arrows on the sides\n\n"
        "Ready to try? Press SPACE to start practice!"
    )

    instruction_text.text = instructions
    instruction_text.draw()
    continue_text.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

# --- 6. Practice Trials ---
if expInfo['Practice Trials']:
    practice_trials = congruent_trials + incongruent_trials
    random.shuffle(practice_trials)

    for trial in practice_trials:
        # Show fixation
        fixation.draw()
        win.flip()
        core.wait(expInfo['ITI Duration (sec)'])

        # Show stimulus
        stimulus_text.text = trial[0]
        stimulus_text.draw()
        win.flip()
        
        # Collect response
        start_time = core.getTime()
        keys = event.waitKeys(keyList=['left', 'right', 'escape'], 
                            maxWait=expInfo['Response Window (sec)'])
        rt = core.getTime() - start_time

        if 'escape' in keys:
            core.quit()

        # Feedback
        if keys:
            correct = (keys[0] == trial[1])
            if correct:
                feedback_text.text = "Great job!"
            else:
                feedback_text.text = "Remember: Look at the middle arrow!"
        else:
            feedback_text.text = "Too slow! Try to respond faster."
        
        feedback_text.draw()
        continue_text.draw()
        win.flip()
        event.waitKeys(keyList=['space'])

# --- 7. Start Main Experiment Instructions ---
instruction_text.text = (
    "Now for the real game!\n\n"
    "• Look at the MIDDLE arrow\n"
    "• Press LEFT for left-pointing arrow\n"
    "• Press RIGHT for right-pointing arrow\n"
    "• Try to be quick but accurate\n"
    "• Take a deep breath and focus"
)
instruction_text.draw()
continue_text.draw()
win.flip()
event.waitKeys(keyList=['space'])

# --- 8. Main Trials ---
main_trials = (congruent_trials * (expInfo['Number of Main Trials'] // 2) +
              incongruent_trials * (expInfo['Number of Main Trials'] // 2))
random.shuffle(main_trials)

for i, trial in enumerate(main_trials):
    # Show fixation
    fixation.draw()
    win.flip()
    core.wait(expInfo['ITI Duration (sec)'])

    # Show stimulus
    stimulus_text.text = trial[0]
    stimulus_text.draw()
    win.flip()
    
    # Collect response
    start_time = core.getTime()
    keys = event.waitKeys(keyList=['left', 'right', 'escape'], 
                        maxWait=expInfo['Response Window (sec)'])
    rt = core.getTime() - start_time

    if 'escape' in keys:
        break

    # Save data
    thisExp.addData('trial', i + 1)
    thisExp.addData('stimulus', trial[0])
    thisExp.addData('correct_response', trial[1])
    thisExp.addData('response', keys[0] if keys else '')
    thisExp.addData('rt', rt if keys else '')
    thisExp.addData('correct', int(keys[0] == trial[1]) if keys else 0)
    thisExp.addData('congruent', int(trial in congruent_trials))
    thisExp.nextEntry()

# --- 9. Goodbye Screen ---
instruction_text.text = (
    "All done! Thank you for playing!\n\n"
    "You did a great job with the arrows!\n"
    "You may now close the window."
)
instruction_text.draw()
continue_text.draw()
win.flip()
event.waitKeys(keyList=['space'])

# --- 10. Save and Exit ---
try:
    thisExp.saveAsWideText(filename + '.csv')
    # Show success message
    instruction_text.text = f"Data saved successfully to:\n{filename}.csv\n\nYou may now close the window."
    instruction_text.draw()
    continue_text.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
except Exception as e:
    # Show error message if saving fails
    instruction_text.text = f"Error saving data: {str(e)}\n\nPress any key to exit."
    instruction_text.draw()
    continue_text.draw()
    win.flip()
    event.waitKeys()

win.close()
core.quit() 