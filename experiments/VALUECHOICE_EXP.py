# --- Value Choice Experiment with Clickable Buttons ---  
from psychopy import visual, core, event, gui, data  
import random  
import os  
import argparse

# --- 1. Parse command-line arguments (for web/app integration) ---
parser = argparse.ArgumentParser()
parser.add_argument('--participant_id', type=str, default='')
parser.add_argument('--session', type=str, default='1')
parser.add_argument('--show_instructions', type=str, default='True')
parser.add_argument('--practice_trials', type=str, default='True')
parser.add_argument('--trial_duration_sec', type=str, default='5.0')
parser.add_argument('--feedback_duration_sec', type=str, default='2.0')
parser.add_argument('--randomize_position', type=str, default='True')
parser.add_argument('--number_of_trials', type=str, default='5')
args, unknown = parser.parse_known_args()

# --- 2. Build expInfo dict from args (convert types as needed) ---
expInfo = {
    'Participant ID': args.participant_id,
    'Session': args.session,
    'Show Instructions': args.show_instructions.lower() in ('true', '1', 'yes'),
    'Practice Trials': args.practice_trials.lower() in ('true', '1', 'yes'),
    'Trial Duration (sec)': float(args.trial_duration_sec),
    'Feedback Duration (sec)': float(args.feedback_duration_sec),
    'Randomize Position': args.randomize_position.lower() in ('true', '1', 'yes'),
    'Number of Trials': int(args.number_of_trials)
}

# --- 3. Data file setup ---  
try:  
    current_dir = os.path.dirname(os.path.abspath(__file__))  
    parent_dir  = os.path.dirname(current_dir)  
    data_dir    = os.path.join(parent_dir, 'data')  
    os.makedirs(data_dir, exist_ok=True)  
    filename = os.path.join(  
        data_dir,  
        f"VALUECHOICE_{expInfo['Participant ID']}_{expInfo['Session']}"  
    )  
    thisExp = data.ExperimentHandler(dataFileName=filename)  
except Exception as e:  
    print(f"Error setting up data directory: {e}")  
    core.quit()  

# --- 4. Create Window and Stimuli ---  
win = visual.Window(size=(1024, 768), color="white", units="pix", fullscr=False)  
instruction_text = visual.TextStim(win, text='', color='black', wrapWidth=800)  
feedback_text    = visual.TextStim(win, text='', color='green', wrapWidth=800)  
mouse_obj        = event.Mouse(win=win)  

# Prompt at top of trial screen  
prompt = visual.TextStim(  
    win,  
    text="Choose one of the two options:",  
    pos=(0, 350),    # y-coordinate above the cards  
    color="black",  
    height=24  
)  

# --- 5. Define stimulus pairs ---  
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
number_of_trials = expInfo['Number of Trials']
stim_pairs = stim_pairs[:number_of_trials]  # Trim to requested trial count  

# --- 6. Card and Button setup ---  
card_width, card_height = 500, 300  
left_card  = visual.Rect(  
    win, width=card_width, height=card_height, pos=(-300, 0),  
    fillColor='lightgrey', lineColor='black'  
)  
right_card = visual.Rect(  
    win, width=card_width, height=card_height, pos=(300, 0),  
    fillColor='lightgrey', lineColor='black'  
)  
left_text  = visual.TextStim(win, text='', pos=(-300, 0), color='black', wrapWidth=400)  
right_text = visual.TextStim(win, text='', pos=(300, 0), color='black', wrapWidth=400)  

# Buttons under each card  
button_width, button_height = 200, 60  
button_left  = visual.Rect(  
    win, width=button_width, height=button_height, pos=(-300, -200),  
    fillColor='darkgrey', lineColor='black'  
)  
button_right = visual.Rect(  
    win, width=button_width, height=button_height, pos=(300, -200),  
    fillColor='darkgrey', lineColor='black'  
)  
btn_text_left  = visual.TextStim(win, text="I choose this", pos=(-300, -200), color='black')  
btn_text_right = visual.TextStim(win, text="I choose this", pos=(300, -200), color='black')  

def display_cards(text1, text2):  
    """Draw prompt, cards, buttons, and text, then flip."""  
    prompt.draw()  
    left_card.draw();  right_card.draw()  
    button_left.draw(); button_right.draw()  
    left_text.text = text1;  right_text.text = text2  
    left_text.draw(); right_text.draw()  
    btn_text_left.draw(); btn_text_right.draw()  
    win.flip()  

def get_card_clicked():  
    """Wait up to trial duration; return side clicked and RT."""  
    mouse_obj.clickReset()  
    timer = core.Clock()  
    while timer.getTime() < float(expInfo['Trial Duration (sec)']):  
        if mouse_obj.isPressedIn(button_left):  
            return 'left', timer.getTime()  
        elif mouse_obj.isPressedIn(button_right):  
            return 'right', timer.getTime()  
    return 'none', float(expInfo['Trial Duration (sec)'])  

# --- 7. Numbered-step Instructions ---  
if expInfo['Show Instructions']:  
    instruction_text.text = (  
        "Welcome to the Value Choice Experiment!\n\n"  
        "In this study you will:\n"  
        "  1. See a screen with two options (cards).\n"  
        "  2. Click the “I choose this” button under the option you prefer.\n"  
        "Press SPACE when you’re ready to begin."  
    )  
    instruction_text.draw()  
    win.flip()  
    event.waitKeys(keyList=['space'])  

# --- 8. Practice Trial ---  
if expInfo['Practice Trials']:  
    practice_pair = ("Receive $10 today", "Receive $15 in one week")  
    instruction_text.text = "Let's practice! Click the button under the card you prefer."  
    instruction_text.draw()  
    win.flip()  
    core.wait(1)  
    display_cards(*practice_pair)  
    side, rt = get_card_clicked()  
    if side == 'left':  
        choice = practice_pair[0]  
    elif side == 'right':  
        choice = practice_pair[1]  
    else:  
        choice = 'No response'  
    feedback_text.text = f"You picked:\n{choice}\n\nPress SPACE to continue."  
    feedback_text.draw()  
    win.flip()  
    event.waitKeys(keyList=['space'])  

# --- 9. Ready Message ---  
instruction_text.text = (  
    f"Now it's time for the real choices.\n\n"  
    f"There will be {number_of_trials} trials.\n"  
    "Take your time, and click on the button under your preferred option.\n\n"  
    "Press SPACE to begin."  
)  
instruction_text.draw()  
win.flip()  
event.waitKeys(keyList=['space'])  

# --- 10. Main Trials ---  
for i, (stim1, stim2) in enumerate(stim_pairs):  
    # randomize left/right if requested  
    if expInfo['Randomize Position'] and random.choice([True, False]):  
        left_stim, right_stim = stim2, stim1  
    else:  
        left_stim, right_stim = stim1, stim2  

    display_cards(left_stim, right_stim)  
    side, rt = get_card_clicked()  

    if side == 'none':  
        choice      = 'No response'  
        feedback_msg = (  
            "No response detected.\n"  
            "Please try to make a choice next time!"  
        )  
    else:  
        choice      = left_stim if side=='left' else right_stim  
        feedback_msg = f"You picked:\n{choice}"  

    # Log data  
    thisExp.addData('trial',        i+1)  
    thisExp.addData('left_option',  left_stim)  
    thisExp.addData('right_option', right_stim)  
    thisExp.addData('choice',       choice)  
    thisExp.addData('side_chosen',  side)  
    thisExp.addData('reaction_time', round(rt,3))  
    thisExp.nextEntry()  

    # Show feedback  
    feedback_text.text = feedback_msg  
    feedback_text.draw()  
    win.flip()  
    core.wait(float(expInfo['Feedback Duration (sec)']))  

# --- 11. Goodbye & Save ---  
instruction_text.text = (  
    "Thank you! Your responses have been recorded.\n\n"  
    "You may now close the window."  
)  
instruction_text.draw()  
win.flip()  
core.wait(3)  

try:  
    thisExp.saveAsWideText(filename + '.csv')  
except Exception as e:  
    instruction_text.text = f"Error saving data: {e}\nPress any key to exit."  
    instruction_text.draw()  
    win.flip()  
    event.waitKeys()  

win.close()  
core.quit()
