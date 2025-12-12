
# specify BIDS root directory
bids_root = "ds005841-download"
# root of derivates directory in which the pipeline will store the processing results
deriv_root = "output/ds005841"

anno_root = "bad_annotations"

# only analyze subject 001 and regfront for now
subjects = ["001"]
tasks = ["regfront"]  # lumfront, lumperp, regfront, regperp, signalscreen, signalvr

# Filter frequencys specification
highpass = 0.1
lowpass = 40
notch = 50
sample_rate = 256 # resample to 256 Hz

# Bad Channels - Please inspect visually before ICA and add them here
bads = ["P1", "POz", "Pz", "Status", "EXG1", "EXG2", "EXG3", "EXG4", "EXG5", "EXG6", "EXG7", "EXG8"]

