# Immediate & Delayed Memory Task (IMT/DMT) in PsychoPy
# Implements practice + test sessions per Dougherty et al. (2002)

from psychopy import visual, core, event, gui
import random, csv, os

# ===== PARTICIPANT INFO =====
expInfo = {
    'Participant ID': '',
    'Session': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],  # Dropdown menu
    'Show Instructions': True,  # Toggle for instructions
    'Practice Trials': True,    # Toggle for practice
    'Number of Blocks': 2,      # How many blocks per task
    'Block Duration (sec)': 75.0,  # How long each block lasts
    'Rest Duration (sec)': 15.0,   # Time between blocks
    'Stimulus Duration (sec)': 0.5, # How long each number shows
    'Blackout Duration (sec)': 0.5  # Time between numbers
}

dlg = gui.DlgFromDict(expInfo, title="Number Memory Game", 
                     order=['Participant ID', 'Session', 'Show Instructions', 'Practice Trials', 
                           'Number of Blocks', 'Block Duration (sec)', 'Rest Duration (sec)',
                           'Stimulus Duration (sec)', 'Blackout Duration (sec)'])
if not dlg.OK:
    core.quit()

pid = expInfo['Participant ID']
sess = expInfo['Session']

# ===== PARAMETERS =====
# Stimulus properties
nDigits = 5  # length of stimuli
stimDur = expInfo['Stimulus Duration (sec)']
blackoutDur = expInfo['Blackout Duration (sec)']

# Task structure
taskType = 3       # 1=IMT only,2=DMT only,3=IMT->DMT,4=DMT->IMT
nBlocksPerTask = expInfo['Number of Blocks']
blockDur = expInfo['Block Duration (sec)']
restDur = expInfo['Rest Duration (sec)']

# Probabilities (on per-trial basis)
targetProb = 60
catchProb = 0
fillerProb = 40  # must sum to 100
# Constraints
minLatency = 0.1    # min RT accepted (s)
dmtNDistractors = 3 # distractors after target in DMT
minhDist = 2        # min digit differences for filler

distractorString = '1'*nDigits  # e.g. '11111' or '12345'

# ===== SETUP =====
win = visual.Window(fullscr=False, color='white', units='norm')
text = visual.TextStim(win, text='', height=0.1)
clock = core.Clock()

# Data storage
results = []
mouse = event.Mouse(win=win)

# ===== UTILS =====
def gen_random_number(prev=None, kind='filler'):
    """Generate a random nDigits string based on kind."""
    if kind=='target' and prev:
        return prev
    if kind=='catch' and prev:
        # change exactly one digit
        s=list(prev)
        idx = random.randrange(nDigits)
        digit = str((int(s[idx])+random.randint(1,9))%10)
        s[idx] = digit
        return ''.join(s)
    # filler: differ by >=minhDist
    while True:
        s=''.join(str(random.randint(0,9)) for _ in range(nDigits))
        if prev:
            dist=sum(a!=b for a,b in zip(s,prev))
            if dist>=minhDist and s!=distractorString:
                return s
        else:
            if s!=distractorString:
                return s


def run_block(block_mode, block_idx):
    """
    Run one block:
    block_mode: 'IMT' or 'DMT'
    """
    nTrials = int(blockDur/(stimDur+blackoutDur))
    # initialize first stimulus
    prev = gen_random_number(None,'filler')
    clock.reset()
    startTime = core.getTime()
    results.append({'participant':pid,'session':sess,'block':block_idx,
                    'mode':block_mode,'trial':0,'stim':prev,
                    'resp':False,'correct':False,'rt':None})
    trial_count = 1
    next_distractors = 0
    while core.getTime() - startTime < blockDur:
        # determine trial type
        if block_mode=='DMT' and next_distractors>0:
            stim = distractorString
            kind = 'distractor'
            next_distractors -= 1
        else:
            r = random.uniform(0,100)
            if r<targetProb and prev is not None:
                stim = prev; kind='target';
                if block_mode=='DMT':
                    next_distractors = dmtNDistractors
            elif r<targetProb+catchProb:
                stim = gen_random_number(prev,'catch'); kind='catch'
            else:
                stim = gen_random_number(prev,'filler'); kind='filler'
        # present stimulus
        text.text = stim; text.draw(); win.flip()
        clock.reset(); responded=False; rt=None
        while clock.getTime() < stimDur:
            buttons = mouse.getPressed()
            if any(buttons) and not responded:
                responded=True; rt=clock.getTime()
            core.wait(0.01)
        # blackout
        win.flip(); core.wait(blackoutDur)
        # determine correctness
        correct = False
        if kind=='target' and responded and rt>=minLatency: correct=True
        if kind!='target' and not responded: correct=True
        results.append({'participant':pid,'session':sess,'block':block_idx,
                        'mode':block_mode,'trial':trial_count,'stim':stim,
                        'resp':responded,'correct':correct,'rt':rt})
        prev = stim if kind!='distractor' else prev
        trial_count+=1
    # rest
    text.text='Rest'; text.draw(); win.flip(); core.wait(restDur)

# ===== MAIN =====
# Calculate total duration
practice_blocks = 1  # One practice block
test_blocks = nBlocksPerTask * (2 if taskType in [3,4] else 1)  # Number of test blocks
total_blocks = practice_blocks + test_blocks
total_time = total_blocks * (blockDur + restDur)  # Total time in seconds
total_minutes = int(total_time / 60)
total_seconds = int(total_time % 60)

# Show instructions
if expInfo['Show Instructions']:
    instructions = (
        "Welcome to the Number Matching Game!\n\n"
        "Here's how to play:\n"
        "• You'll see two numbers\n"
        "• If they match, press 'S'\n"
        "• If they don't match, press 'L'\n"
        "• Try to be quick but accurate\n\n"
        "Ready to try? Press any key to start practice!"
    )

    text.text = instructions
    text.draw()
    win.flip()
    event.waitKeys()

# practice session
if expInfo['Practice Trials']:
    if taskType in (1,4):
        run_block('IMT','P1')
    if taskType in (2,3):
        run_block('DMT','P1')

# test session
order = []
if taskType==1: order=['IMT']*nBlocksPerTask
elif taskType==2: order=['DMT']*nBlocksPerTask
elif taskType==3: order=['IMT','DMT']*nBlocksPerTask
else: order=['DMT','IMT']*nBlocksPerTask

text.text = (
    "Now for the real game!\n\n"
    "• Press 'S' for matching numbers\n"
    "• Press 'L' for different numbers\n"
    "• Try to be quick but accurate\n"
    "• Take a deep breath and focus\n\n"
    "Ready? Press any key to begin!"
)
text.draw()
win.flip()
event.waitKeys()

for idx,mode in enumerate(order, start=1): run_block(mode,idx)

# save data
parent = os.path.join('..','data')
if not os.path.exists(parent): os.makedirs(parent)
fpath = os.path.join(parent, f"IMTDMT_{pid}_{sess}.csv")
with open(fpath,'w',newline='') as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader(); writer.writerows(results)

# end
text.text = (
    "All done! Thank you for playing!\n\n"
    "You did a great job with the numbers!\n"
    "You may now close the window."
)
text.draw()
win.flip()
core.wait(3.0)

win.close()
core.quit() 