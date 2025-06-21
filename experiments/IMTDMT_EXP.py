# Immediate & Delayed Memory Task (IMT/DMT) in PsychoPy
# Simplified: only essential parameters, streamlined flow, with DMT distractor page and grouped main rounds

from psychopy import visual, core, event, gui
import random, csv, os, datetime

import argparse

# === Load configured parameters from CLI flags ===
parser = argparse.ArgumentParser()
parser.add_argument('--participant_id',                 type=str, default='')
parser.add_argument('--session',                        type=str, default='1')
parser.add_argument('--show_instructions',              type=str, default='True')
parser.add_argument('--practice_trials',                type=str, default='True')
parser.add_argument('--number_of_imt_practice_trials',  type=str, default='2')
parser.add_argument('--number_of_dmt_practice_trials',  type=str, default='2')
parser.add_argument('--number_of_imt_experiment_trials',type=str, default='15')
parser.add_argument('--number_of_dmt_experiment_trials',type=str, default='15')
parser.add_argument('--stimulus_duration_s',            type=str, default='2.0')
parser.add_argument('--task_order',                     type=str,
                    choices=['IMT->DMT','DMT->IMT','IMT only','DMT only'],
                    default='IMT->DMT')
args = parser.parse_args()

# Build expInfo dict from args (convert types as needed)
expInfo = {
    'Participant ID':             args.participant_id,
    'Session':                    args.session,
    'Show Instructions':          args.show_instructions.lower() in ('true','1','yes'),
    'Practice Trials':            args.practice_trials.lower() in ('true','1','yes'),
    'Number of IMT Practice Trials':  int(args.number_of_imt_practice_trials),
    'Number of DMT Practice Trials':  int(args.number_of_dmt_practice_trials),
    'Number of IMT Experiment Trials': int(args.number_of_imt_experiment_trials),
    'Number of DMT Experiment Trials': int(args.number_of_dmt_experiment_trials),
    'Stimulus Duration (s)':      float(args.stimulus_duration_s),
    'Task Order':                 args.task_order
}


# Fixed parameters (not exposed)
BLACKOUT = 2.0          # seconds blank between stimuli
REST = 3.0              # seconds rest after each block
MIN_RT = 0.1            # minimal valid RT (s)
RESPONSE_TIMEOUT = 5.0  # seconds to wait for response
N_DIGITS = 5
DISTRACTOR = '12345'[:N_DIGITS]
DMT_DISTRACTORS = 3     # number of distractors in DMT
TARGET_PROB = 60
CATCH_PROB = 0
FILLER_PROB = 40
STIM_SIZE = 0.1         # font height

# Setup window and stimuli
win = visual.Window(fullscr=False, color='white', units='norm')
text = visual.TextStim(win, '', height=STIM_SIZE, color='black', wrapWidth=1.5)
feedback = visual.TextStim(win, '', height=0.08, color='blue', wrapWidth=1.5)
clock = core.Clock()
results = []

# Helpers: safe convert
safe_int = lambda v,d: int(v) if str(v).isdigit() else d
safe_float = lambda v,d: float(v) if str(v).replace('.','',1).isdigit() else d

# Extract parameters
stimDur = safe_float(expInfo['Stimulus Duration (s)'], 2.0)
nIMT_practice = safe_int(expInfo['Number of IMT Practice Trials'], 2)
nDMT_practice = safe_int(expInfo['Number of DMT Practice Trials'], 2)
nIMT_main = safe_int(expInfo['Number of IMT Experiment Trials'], 15)
nDMT_main = safe_int(expInfo['Number of DMT Experiment Trials'], 15)
pid = expInfo['Participant ID']
sess = expInfo['Session']

# Generate a random n-digit number

def gen_num(prev=None, kind='filler'):
    if kind=='target' and prev:
        return prev
    if kind=='catch' and prev:
        s=list(prev)
        i=random.randrange(N_DIGITS)
        s[i]=str((int(s[i])+random.randint(1,9))%10)
        return ''.join(s)
    while True:
        s=''.join(str(random.randint(0,9)) for _ in range(N_DIGITS))
        if not prev or (sum(a!=b for a,b in zip(s,prev))>=2 and s!=DISTRACTOR):
            return s

# Run a block of trials

def run_block(mode, label, trials, practice=False):
    # Title
    title = "Immediate Memory Task (IMT)" if mode=='IMT' else "Delayed Memory Task (DMT)"
    text.text = title
    text.draw(); win.flip(); core.wait(2)

    # In DMT practice, demonstrate distractor
    if practice and mode=='DMT':
        text.text = f"Practice DMT uses distractor."
        text.draw(); win.flip(); core.wait(3)

    prev = gen_num(None, 'filler')
    for t in range(1, trials+1):
        r=random.uniform(0,100)
        if r < TARGET_PROB:
            stim, kind = prev, 'target'
        elif r < TARGET_PROB + CATCH_PROB:
            stim, kind = gen_num(prev, 'catch'), 'catch'
        else:
            stim, kind = gen_num(prev, 'filler'), 'filler'

        # show previous stimulus
        text.text = prev; text.draw(); win.flip(); core.wait(stimDur)
        win.flip(); core.wait(BLACKOUT)

        # DMT distractors for target
        if mode=='DMT' and kind=='target':
            for _ in range(DMT_DISTRACTORS):
                text.text = DISTRACTOR; text.draw(); win.flip(); core.wait(stimDur)
                win.flip(); core.wait(BLACKOUT)

        # show current stimulus
        text.text = stim; text.draw(); win.flip(); core.wait(stimDur)
        win.flip(); core.wait(BLACKOUT)

        # response prompt with timeout
        text.text = "Press 'S' if same, 'D' if different"
        text.draw(); win.flip()
        clock.reset()
        keys = event.waitKeys(maxWait=RESPONSE_TIMEOUT, keyList=['s','d'])
        if keys:
            key = keys[0]; rt = clock.getTime(); no_response=False
        else:
            key = None; rt = None; no_response=True
            text.text = "No response detected! Please respond on time."; text.draw(); win.flip(); core.wait(2)

        win.flip(); core.wait(BLACKOUT)

        if no_response:
            correct=False
        else:
            correct = (kind=='target' and key=='s' and rt>=MIN_RT) or (kind!='target' and key=='d')

        # record data
        results.append({
            'pid': pid,
            'sess': sess,
            'block': label,
            'trial': t,
            'prev': prev,
            'curr': stim,
            'kind': kind,
            'key': key,
            'correct': correct,
            'rt': rt
        })

        # practice feedback
        if practice:
            feedback.text = 'Correct!' if correct else 'Wrong!'
            feedback.draw(); win.flip(); core.wait(1)

        prev = stim

    # end-of-block pause (only main rounds)
    if not practice:
        text.text = f"{mode} block '{label}' complete"; text.draw(); win.flip(); core.wait(REST)

# Instructions text
if expInfo['Show Instructions']:
    text.text = (
        "Number Matching Experiment:\n"
        "You will be shown two numbers. Press 'S' if same, 'D' if different.\n"
        "1. In IMT (Immediate Memory Task), match the second number with the first.\n"
        "2. In DMT (Delayed Memory Task): sometimes there will be 3 'distractors numbers,'\n"
        "sometimes not, please match the last number with the first one."
    )
    text.draw(); win.flip(); event.waitKeys()

# Practice session
if expInfo['Practice Trials']:
    for i in range(1, nIMT_practice+1):
        run_block('IMT', f'P-IMT-{i}', 1, practice=True)
    for i in range(1, nDMT_practice+1):
        run_block('DMT', f'P-DMT-{i}', 1, practice=True)
    text.text = "Practice complete. Press any key to begin main experiment."; text.draw(); win.flip(); event.waitKeys()

# Main experiment grouped
order = expInfo['Task Order']
if order == 'IMT->DMT':
    run_block('IMT', 'Main-IMT', nIMT_main)
    text.text = "IMT main complete. Press any key for DMT."; text.draw(); win.flip(); event.waitKeys()
    run_block('DMT', 'Main-DMT', nDMT_main)
elif order == 'DMT->IMT':
    run_block('DMT', 'Main-DMT', nDMT_main)
    text.text = "DMT main complete. Press any key for IMT."; text.draw(); win.flip(); event.waitKeys()
    run_block('IMT', 'Main-IMT', nIMT_main)
elif order == 'IMT only':
    run_block('IMT', 'Main-IMT', nIMT_main)
elif order == 'DMT only':
    run_block('DMT', 'Main-DMT', nDMT_main)

# Save data to parent directory
os.makedirs(os.path.join('..','data'), exist_ok=True)
fname = f"imtdmt_{pid}_{sess}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
with open(os.path.join('..','data', fname), 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader(); writer.writerows(results)

# Completion message
text.text = "Thank you for participating!"; text.draw(); win.flip(); core.wait(3)
win.close(); core.quit()
