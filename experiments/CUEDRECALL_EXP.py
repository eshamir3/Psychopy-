# --- Cued Recall Task ---
# Implements the Tolan & Tehan (1999) variant as described in the Inquisit manual

from psychopy import visual, core, event, gui, data
from psychopy.visual import TextBox2
import random
import os

# --- 1. Participant Info ---
expInfo = {
    'Participant ID': '',
    'Session': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],  # Dropdown menu
    'Show Instructions': True,  # Toggle for instructions
    'Practice Trials': True,    # Toggle for practice
    'Number of Practice Trials': 2,  # How many practice trials
    'Number of Main Trials': 12,     # How many main trials
    'Word Display Time (sec)': 0.5,  # How long each word shows
    'Number Task Time (sec)': 1.0,   # Time for number comparison
    'Recall Time (sec)': 5.0         # Time to type answer
}

dlg = gui.DlgFromDict(expInfo, title="Word Memory Game", 
                     order=['Participant ID', 'Session', 'Show Instructions', 'Practice Trials', 
                           'Number of Practice Trials', 'Number of Main Trials', 
                           'Word Display Time (sec)', 'Number Task Time (sec)', 'Recall Time (sec)'])
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
    
    filename = os.path.join(data_dir, f"CUEDRECALL_{expInfo['Participant ID']}_{expInfo['Session']}")
    thisExp = data.ExperimentHandler(dataFileName=filename)
except Exception as e:
    print(f"Error setting up data directory: {str(e)}")
    core.quit()

# --- 3. Parameters ---
# Demo timings (s)
getReadyDemo = 3.0
instructDemo = 3.0
distractorDemo = expInfo['Number Task Time (sec)']
recallTimeoutDemo = expInfo['Recall Time (sec)']
stimDemo = expInfo['Word Display Time (sec)']

# Test timings (s)
getReadyTest = 1.0
instructTest = 1.0
distractorTest = expInfo['Number Task Time (sec)']
recallTimeoutTest = expInfo['Recall Time (sec)']
stimTest = expInfo['Word Display Time (sec)']
iti = 0.5

# Keys for distractor
keySmaller = 's'
keyLarger = 'l'

# Example stimuli (customize as needed)
categories = {
    'bird': {'target': 'penguin', 'foil': 'robin', 'fillers': ['eagle', 'falcon', 'parrot', 'hawk']},
    'fruit': {'target': 'banana', 'foil': 'apple', 'fillers': ['grape', 'mango', 'pear', 'orange']},
    'furniture': {'target': 'chair', 'foil': 'couch', 'fillers': ['table', 'stool', 'desk', 'bench']},
    'animal': {'target': 'tiger', 'foil': 'lion', 'fillers': ['bear', 'wolf', 'fox', 'deer']},
    'color': {'target': 'purple', 'foil': 'blue', 'fillers': ['green', 'yellow', 'orange', 'pink']},
    'job': {'target': 'doctor', 'foil': 'teacher', 'fillers': ['nurse', 'chef', 'driver', 'artist']}
}

# --- 4. Create Window and Stimuli ---
win = visual.Window(size=(1024, 768), 
                   color='white', 
                   units='pix',  # Use pixels for more consistent sizing
                   fullscr=False,
                   allowGUI=True)  # Allow GUI for better window management

# Calculate text sizes based on screen dimensions
text_height = 25  # Even smaller font
wrap_width = 900  # Keep the wider width

instruction_text = visual.TextStim(win, 
                                 text='', 
                                 height=text_height, 
                                 wrapWidth=wrap_width,
                                 color='black')
text = visual.TextStim(win, 
                      text='', 
                      height=text_height, 
                      wrapWidth=wrap_width,
                      color='black')
input_box = TextBox2(win, 
                    text='', 
                    pos=(0, 0), 
                    letterHeight=text_height * 0.8,
                    size=(wrap_width, text_height * 2),
                    borderColor='black', 
                    fillColor='white', 
                    color='black')
clock = core.Clock()

# --- 5. Show Instructions ---
if expInfo['Show Instructions']:
    instructions = (
        "Welcome to the Word Memory Game!\n\n"
        "Here's how to play:\n"
        "• You'll see pairs of words\n"
        "• Try to remember which words go together\n"
        "• Later, you'll see one word and need to type its partner\n\n"
        "Ready to try? Press any key to start practice!"
    )

    instruction_text.text = instructions
    instruction_text.draw()
    win.flip()
    event.waitKeys()

# --- 6. Functions ---
def show_msg(msg, wait_key=True, duration=None):
    text.text = msg
    text.draw()
    win.flip()
    if wait_key:
        event.waitKeys()
    elif duration:
        core.wait(duration)

def present_words(words, duration):
    for w in words:
        text.text = w
        text.draw()
        win.flip()
        core.wait(duration)

def run_demo(trial_type):
    rec = {'participant': expInfo['Participant ID'], 'session': expInfo['Session'],
           'trialType': 'demo1' if trial_type == 0 else 'demo2'}
    cat = random.choice(list(categories.keys()))
    info = categories[cat]
    rec['category'] = cat
    
    # Block1 or foil block
    if trial_type == 0:
        block1 = info['fillers'] + [info['target']]
    else:
        block1 = info['fillers'][:2] + [info['foil']] + info['fillers'][2:]
    random.shuffle(block1)
    
    show_msg('Get ready (Demo)', wait_key=False, duration=getReadyDemo)
    show_msg('Say aloud (Demo)', wait_key=False, duration=instructDemo)
    present_words(block1, stimDemo)
    
    if trial_type == 1:
        show_msg('Read silently (Demo)', wait_key=False, duration=instructDemo)
        block2 = info['fillers'][:2] + [info['target']] + info['fillers'][2:]
        random.shuffle(block2)
        present_words(block2, stimDemo)
    
    # Distractor demo
    show_msg('Now complete the number comparison task.\nPress s for smaller than 50, l for larger than 50.', 
             wait_key=True, duration=None)
    
    for _ in range(8):
        num = random.randint(10, 99)
        text.text = str(num)
        text.draw()
        win.flip()
        event.waitKeys(maxWait=distractorDemo, keyList=[keySmaller, keyLarger])
    
    # Recall demo
    show_msg(f'Now try to recall the target word from the category: {cat}\nType your answer and press Enter.', 
             wait_key=True, duration=None)
    
    input_box.text = ''
    clock.reset()
    ans = ''
    while clock.getTime() < recallTimeoutDemo:
        input_box.text = ans
        input_box.draw()
        win.flip()
        keys = event.getKeys()
        if 'return' in keys:
            break
        for k in keys:
            if k == 'backspace':
                ans = ans[:-1]
            elif len(k) == 1 and k.isalpha():
                ans += k
    
    rec['recallResponse'] = ans.lower().strip()
    thisExp.addData('trial_type', rec['trialType'])
    thisExp.addData('category', rec['category'])
    thisExp.addData('recall_response', rec['recallResponse'])
    thisExp.nextEntry()
    
    # Show feedback
    if rec['recallResponse'] == info['target']:
        feedback = f"Great job! You remembered: {info['target']} 🎉"
    else:
        feedback = f"Almost! The word was: {info['target']} 💪"
    show_msg(feedback, wait_key=True, duration=None)
    
    core.wait(iti)

def run_test(trial_type, idx):
    rec = {'participant': expInfo['Participant ID'], 'session': expInfo['Session'], 'trialNum': idx,
           'trialType': {2: 'block2_target', 3: 'block2_control', 4: 'block1'}[trial_type]}
    cat = random.choice(list(categories.keys()))
    info = categories[cat]
    rec.update({'category': cat, 'target': info['target'], 'foil': info['foil']})
    
    # Build blocks
    if trial_type == 2:  # Two lists: first with foil, second with target
        block1 = info['fillers'][:2] + [info['foil']] + info['fillers'][2:]
        block2 = info['fillers'][:2] + [info['target']] + info['fillers'][2:]
    elif trial_type == 3:  # Two lists: first random, second with target
        block1 = random.sample(info['fillers'], 4)
        block2 = info['fillers'][:2] + [info['target']] + info['fillers'][2:]
    else:  # One list with target
        block1 = info['fillers'][:2] + [info['target']] + info['fillers'][2:]
        block2 = []  # No second list for block1 trials
    
    random.shuffle(block1)
    if block2:
        random.shuffle(block2)
    
    # Record block contents
    rec['block1_words'] = ','.join(block1)
    if block2:
        rec['block2_words'] = ','.join(block2)
    else:
        rec['block2_words'] = ''
    
    # Present first list
    show_msg('Get ready', wait_key=False, duration=getReadyTest)
    show_msg('Say these words aloud', wait_key=False, duration=instructTest)
    present_words(block1, stimTest)
    
    # Present second list (if any)
    if block2:
        show_msg('Now read these words silently', wait_key=False, duration=instructTest)
        present_words(block2, stimTest)
    
    # Distractor
    show_msg('Complete the number comparison task.\nPress s for smaller than 50, l for larger than 50.', 
             wait_key=True, duration=None)
    
    dist = []
    for _ in range(8):
        num = random.randint(10, 99)
        text.text = str(num)
        text.draw()
        win.flip()
        clock.reset()
        keys = event.waitKeys(maxWait=distractorTest,
                            keyList=[keySmaller, keyLarger], timeStamped=clock)
        if keys:
            dist.append((num, keys[0][0], keys[0][1]))
        else:
            dist.append((num, '', -1))
    
    rec['distractorData'] = str(dist)  # Convert to string for CSV storage
    
    # Recall
    if block2:  # If there was a second list, recall from that
        show_msg(f'Category: {cat}\nType the word from the second list and press Enter.', 
                 wait_key=True, duration=None)
        correct_answer = info['target']
    else:  # If no second list, recall from first list
        show_msg(f'Category: {cat}\nType the word from the list and press Enter.', 
                 wait_key=True, duration=None)
        correct_answer = info['target']
    
    input_box.text = ''
    clock.reset()
    ans = ''
    while clock.getTime() < recallTimeoutTest:
        input_box.text = ans
        input_box.draw()
        win.flip()
        keys = event.getKeys()
        if 'return' in keys:
            break
        for k in keys:
            if k == 'backspace':
                ans = ans[:-1]
            elif len(k) == 1 and k.isalpha():
                ans += k
    
    rec['recallResponse'] = ans.lower().strip()
    rec['correct'] = int(rec['recallResponse'] == correct_answer)
    rec['recallRT'] = int(clock.getTime() * 1000)
    
    # Save data
    thisExp.addData('trial_num', rec['trialNum'])
    thisExp.addData('trial_type', rec['trialType'])
    thisExp.addData('category', rec['category'])
    thisExp.addData('target', rec['target'])
    thisExp.addData('foil', rec['foil'])
    thisExp.addData('block1_words', rec['block1_words'])
    thisExp.addData('block2_words', rec['block2_words'])
    thisExp.addData('recall_response', rec['recallResponse'])
    thisExp.addData('correct', rec['correct'])
    thisExp.addData('recall_rt', rec['recallRT'])
    thisExp.addData('distractor_data', rec['distractorData'])
    thisExp.nextEntry()
    
    # No feedback for test trials
    core.wait(iti)

# --- 7. Run Practice Trials ---
for t in (0, 1):
    run_demo(t)

# --- 8. Show Main Experiment Instructions ---
instruction_text.text = (
    "Now for the real game!\n\n"
    "• Remember which words go together\n"
    "• Type the matching word when you see its partner\n"
    "• Take a deep breath and focus\n\n"
    "Ready? Press any key to begin!"
)
instruction_text.draw()
win.flip()
event.waitKeys()

# --- 9. Run Main Trials ---
# Full version: 36 trials (12 of each type)
# trial_types = [2] * 12 + [3] * 12 + [4] * 12

# Shorter version: 12 trials (4 of each type)
trial_types = [2] * 4 + [3] * 4 + [4] * 4
random.shuffle(trial_types)
for i, tt in enumerate(trial_types, 1):
    run_test(tt, i)

# --- 10. Goodbye Screen ---
instruction_text.text = (
    "All done! Thank you for playing!\n\n"
    "You did a great job with the words!\n"
    "You may now close the window."
)
instruction_text.draw()
win.flip()
core.wait(3.0)

win.close()
core.quit()
