# Cued Recall Procedure in PsychoPy
# Implements the Tolan & Tehan (1999) variant as described in the Inquisit manual

from psychopy import visual, core, event, gui
from psychopy.visual import TextBox2
import random, csv, os

# ============ PARTICIPANT INFO DIALOG ============
info = {'Participant ID': '', 'Session': '1'}
dlg = gui.DlgFromDict(info, title='Cued Recall Task')
if not dlg.OK:
    core.quit()
participant_id = info['Participant ID']
session_id = info['Session']

# ============ PARAMETERS ============
# Demo timings (s)
getReadyDemo      = 10.0
instructDemo      = 10.0
distractorDemo    = 10.0
recallTimeoutDemo= 20.0
stimDemo          = 5.0

# Test timings (s)
getReadyTest      = 3.0
instructTest      = 1.0
distractorTest    = 1.0
recallTimeoutTest= 5.0
stimTest          = 1.0
iti               = 0.5

# Keys for distractor
keySmaller = 's'
keyLarger  = 'l'

# Example stimuli (customize as needed)
categories = {
    'bird':      {'target':'penguin','foil':'robin',  'fillers':['eagle','falcon']},
    'fruit':     {'target':'banana', 'foil':'apple',  'fillers':['grape','mango']},
    'furniture': {'target':'chair',  'foil':'couch',  'fillers':['table','stool']}
}

# ============ SETUP ============
win = visual.Window(fullscr=False, color='white', units='height')
text     = visual.TextStim(win, text='', height=0.07, wrapWidth=1.2)
input_box= TextBox2(win, text='', pos=(0,0), letterHeight=0.06,
                   size=(1.2,0.15), borderColor='black', fillColor='white', color='black')
clock    = core.Clock()
results  = []

# ============ FUNCTIONS ============
def show_msg(msg, wait_key=True, duration=None):
    text.text = msg
    text.draw(); win.flip()
    if wait_key:
        event.waitKeys()
    elif duration:
        core.wait(duration)


def present_words(words, duration):
    for w in words:
        text.text = w; text.draw(); win.flip()
        core.wait(duration)


def run_demo(trial_type):
    rec = {'participant':participant_id,'session':session_id,
           'trialType': 'demo1' if trial_type==0 else 'demo2'}
    cat = random.choice(list(categories.keys()))
    info = categories[cat]
    rec['category']=cat
    # Block1 or foil block
    if trial_type==0:
        block1 = info['fillers'] + [info['target']]
    else:
        block1 = info['fillers'][:2] + [info['foil']] + info['fillers'][2:]
    random.shuffle(block1)
    show_msg('Get ready (Demo)', wait_key=False, duration=getReadyDemo)
    show_msg('Say aloud (Demo)', wait_key=False, duration=instructDemo)
    present_words(block1, stimDemo)
    if trial_type==1:
        show_msg('Read silently (Demo)', wait_key=False, duration=instructDemo)
        block2 = info['fillers'][:2] + [info['target']] + info['fillers'][2:]
        random.shuffle(block2)
        present_words(block2, stimDemo)
    # Distractor demo
    for _ in range(8):
        num = random.randint(10,99)
        text.text = str(num); text.draw(); win.flip()
        event.waitKeys(maxWait=distractorDemo, keyList=[keySmaller,keyLarger])
    # Recall demo
    input_box.text=''; clock.reset(); ans=''
    while clock.getTime()<recallTimeoutDemo:
        input_box.text=ans; input_box.draw(); win.flip()
        keys=event.getKeys()
        if 'return' in keys: break
        for k in keys:
            if k=='backspace': ans=ans[:-1]
            elif len(k)==1 and k.isalpha(): ans+=k
    rec['recallResponse']=ans.lower().strip()
    results.append(rec)
    core.wait(iti)


def run_test(trial_type, idx):
    rec={'participant':participant_id,'session':session_id,'trialNum':idx,
         'trialType':{2:'block2_target',3:'block2_control',4:'block1'}[trial_type]}
    cat=random.choice(list(categories.keys())); info=categories[cat]
    rec.update({'category':cat,'target':info['target'],'foil':info['foil']})
    # Build blocks
    if trial_type==2:
        block1=info['fillers'][:2]+[info['foil']]+info['fillers'][2:]
        block2=info['fillers'][:2]+[info['target']]+info['fillers'][2:]
    elif trial_type==3:
        block1=random.sample(info['fillers'],4)
        block2=info['fillers'][:2]+[info['target']]+info['fillers'][2:]
    else:
        block1=[]
        block2=info['fillers'][:2]+[info['target']]+info['fillers'][2:]
    random.shuffle(block1); random.shuffle(block2)
    # Present
    show_msg('Get ready', wait_key=False, duration=getReadyTest)
    show_msg('Say aloud', wait_key=False, duration=instructTest)
    present_words(block1 or block2, stimTest)
    if trial_type in (2,3):
        show_msg('Read silently', wait_key=False, duration=instructTest)
        present_words(block2, stimTest)
    # Distractor
    dist=[]
    for _ in range(8):
        num=random.randint(10,99)
        text.text=str(num); text.draw(); win.flip()
        clock.reset(); keys=event.waitKeys(maxWait=distractorTest,
                         keyList=[keySmaller,keyLarger], timeStamped=clock)
        if keys: dist.append((num,keys[0][0],keys[0][1]))
        else:    dist.append((num,'',-1))
    rec['distractorData']=dist
    # Recall
    input_box.text=''; clock.reset(); ans=''
    while clock.getTime()<recallTimeoutTest:
        input_box.text=ans; input_box.draw(); win.flip()
        keys=event.getKeys()
        if 'return' in keys: break
        for k in keys:
            if k=='backspace': ans=ans[:-1]
            elif len(k)==1 and k.isalpha(): ans+=k
    rec['recallResponse']=ans.lower().strip()
    rec['correct']=int(rec['recallResponse']==info['target'])
    rec['recallRT']=int(clock.getTime()*1000)
    results.append(rec)
    core.wait(iti)

# ===== MAIN =====
show_msg('Welcome! Two demo trials first. Press any key.')
for t in (0,1): run_demo(t)
trial_types=[2]*12+[3]*12+[4]*12; random.shuffle(trial_types)
show_msg('Actual test begins. Press any key.')
for i,tt in enumerate(trial_types,1): run_test(tt,i)

# Save
# Use parent data directory
data_dir = os.path.join('..', 'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
filename = f"CUEDRECALL_{participant_id}_{session_id}.csv"
filepath = os.path.join(data_dir, filename)
with open(filepath, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

show_msg('Complete. Thank you! Press any key.')
win.close(); core.quit()
