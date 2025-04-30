# --- SART Experiment (Modified for Faster Practice) ---
from psychopy import visual, core, event, gui, data
import random
import os

# --- 1. Participant Info ---
expInfo = {'Participant': '', 'Session': '001'}
dlg = gui.DlgFromDict(expInfo, title="SART Experiment")
if not dlg.OK:
    core.quit()

# --- 2. Data file setup ---
filename = f"data/{expInfo['Participant']}_{expInfo['Session']}"
if not os.path.exists('data'):
    os.makedirs('data')

thisExp = data.ExperimentHandler(dataFileName=filename)

# --- 3. Experiment Parameters (FASTER now) ---
stim_duration = 0.35   # seconds stimulus shown (FASTER than before)
isi_duration = 0.5     # inter-stimulus interval (FASTER than before)
target_number = '3'    # number to withhold response
practice_trials = 5    # SHORTER practice (was 10 before)
main_trials = 90       # main experiment unchanged

# --- 4. Create Window and Stimuli ---
win = visual.Window(fullscr=False, color='black')
fixation = visual.TextStim(win, text='+', color='white')
digit_stim = visual.TextStim(win, text='', color='white', height=0.2)
instruction_text = visual.TextStim(win, text='', color='white', wrapWidth=1.5)
feedback_text = visual.TextStim(win, text='', color='white', height=0.1)

# --- 5. Show Instructions ---
instructions = (
    "Welcome to the experiment!\n\n"
    "You will see digits from 0 to 9 appear on the screen.\n"
    "Press the SPACEBAR as fast as you can for every digit,\n"
    "**EXCEPT** when you see the number '3'.\n\n"
    "When you see '3', do NOT press anything.\n\n"
    "Press any key to start practice trials!"
)

instruction_text.text = instructions
instruction_text.draw()
win.flip()
event.waitKeys()

# --- 6. Practice Trials (shorter and faster) ---
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
        feedback_text.text = "Correct!"
    else:
        feedback_text.text = "Incorrect!"
    
    feedback_text.draw()
    win.flip()
    core.wait(0.75)  # Feedback time also a bit shorter

    if any(k[0] == 'escape' for k in keys):
        core.quit()

# --- 7. Start Main Experiment Instructions ---
instruction_text.text = (
    "Now the real experiment will begin.\n\n"
    "Remember: Press SPACEBAR for every number except '3'.\n\n"
    "Try to go as fast and accurately as possible.\n\n"
    "Press any key to begin!"
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
instruction_text.text = "Thank you for participating!\n\nYou may now close the window."
instruction_text.draw()
win.flip()
core.wait(3.0)

# --- 10. Save and Exit ---
thisExp.saveAsWideText(filename + '.csv')
win.close()
core.quit()
