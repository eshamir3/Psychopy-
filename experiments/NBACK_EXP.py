# --- N-Back Task Experiment ---
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
    'N-Back Level': 2,         # How many items back to remember
    'Stimulus Duration (sec)': 0.5,   # How long each letter shows
    'Response Window (sec)': 1.0,     # Time allowed to respond
    'ITI Duration (sec)': 0.5         # Time between trials
}

dlg = gui.DlgFromDict(expInfo, title="N-Back Task", 
                     order=['Participant ID', 'Session', 'Show Instructions', 'Practice Trials', 
                           'Number of Practice Trials', 'Number of Main Trials', 'N-Back Level',
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
    
    filename = os.path.join(data_dir, f"NBACK_{expInfo['Participant ID']}_{expInfo['Session']}")
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
# Letters to use (excluding similar looking ones)
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 
          'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# --- 5. Show Instructions ---
if expInfo['Show Instructions']:
    instructions = (
        f"Welcome to the Memory Game!\n\n"
        f"Here's how to play:\n"
        f"• Letters will appear one at a time\n"
        f"• Press SPACEBAR if the letter matches the one from {expInfo['N-Back Level']} letters ago\n"
        f"• Do NOT press if it's different\n\n"
        f"For example, with 2-back:\n"
        f"A → B → A → (press SPACEBAR!)\n"
        f"A → B → C → (don't press)\n\n"
        f"Ready to try? Press any key to start practice!"
    )

    instruction_text.text = instructions
    instruction_text.draw()
    win.flip()
    event.waitKeys()

# --- 6. Practice Trials ---
if expInfo['Practice Trials']:
    # Create practice sequence with some matches
    practice_sequence = []
    for _ in range(expInfo['Number of Practice Trials']):
        if random.random() < 0.3:  # 30% chance of match
            if len(practice_sequence) >= expInfo['N-Back Level']:
                practice_sequence.append(practice_sequence[-expInfo['N-Back Level']])
            else:
                practice_sequence.append(random.choice(letters))
        else:
            practice_sequence.append(random.choice(letters))

    for i, letter in enumerate(practice_sequence):
        # Show fixation
        fixation.draw()
        win.flip()
        core.wait(expInfo['ITI Duration (sec)'])

        # Show stimulus
        stimulus_text.text = letter
        stimulus_text.draw()
        win.flip()
        
        # Collect response
        start_time = core.getTime()
        keys = event.waitKeys(keyList=['space', 'escape'], 
                            maxWait=expInfo['Response Window (sec)'])
        rt = core.getTime() - start_time

        if 'escape' in keys:
            core.quit()

        # Check if this should have been a match
        should_match = (i >= expInfo['N-Back Level'] and 
                       letter == practice_sequence[i - expInfo['N-Back Level']])

        # Feedback
        if should_match:
            if keys and 'space' in keys:
                feedback_text.text = "Great job!"
            else:
                feedback_text.text = f"Remember: Press SPACEBAR when you see the same letter from {expInfo['N-Back Level']} back!"
        else:
            if not keys:
                feedback_text.text = "Great job!"
            else:
                feedback_text.text = "Remember: Only press SPACEBAR for matches!"
        
        feedback_text.draw()
        win.flip()
        core.wait(0.75)

# --- 7. Start Main Experiment Instructions ---
instruction_text.text = (
    "Now for the real game!\n\n"
    f"• Press SPACEBAR for letters that match {expInfo['N-Back Level']} back\n"
    "• Do NOT press for different letters\n"
    "• Try to be quick but accurate\n"
    "• Take a deep breath and focus\n\n"
    "Ready? Press any key to begin!"
)
instruction_text.draw()
win.flip()
event.waitKeys()

# --- 8. Main Trials ---
# Create main sequence with some matches
main_sequence = []
for _ in range(expInfo['Number of Main Trials']):
    if random.random() < 0.3:  # 30% chance of match
        if len(main_sequence) >= expInfo['N-Back Level']:
            main_sequence.append(main_sequence[-expInfo['N-Back Level']])
        else:
            main_sequence.append(random.choice(letters))
    else:
        main_sequence.append(random.choice(letters))

for i, letter in enumerate(main_sequence):
    # Show fixation
    fixation.draw()
    win.flip()
    core.wait(expInfo['ITI Duration (sec)'])

    # Show stimulus
    stimulus_text.text = letter
    stimulus_text.draw()
    win.flip()
    
    # Collect response
    start_time = core.getTime()
    keys = event.waitKeys(keyList=['space', 'escape'], 
                        maxWait=expInfo['Response Window (sec)'])
    rt = core.getTime() - start_time

    if 'escape' in keys:
        break

    # Check if this should have been a match
    should_match = (i >= expInfo['N-Back Level'] and 
                   letter == main_sequence[i - expInfo['N-Back Level']])

    # Save data
    thisExp.addData('trial', i + 1)
    thisExp.addData('stimulus', letter)
    thisExp.addData('should_match', int(should_match))
    thisExp.addData('response', 'space' if keys and 'space' in keys else '')
    thisExp.addData('rt', rt if keys else '')
    thisExp.addData('correct', int((should_match and keys and 'space' in keys) or 
                                 (not should_match and not keys)))
    thisExp.nextEntry()

# --- 9. Goodbye Screen ---
instruction_text.text = (
    "All done! Thank you for playing!\n\n"
    "You did a great job with the memory game!\n"
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